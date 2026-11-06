"""Check a Pinterest bulk CSV before Matt uploads it. Usage: python validate_csv.py <csv> <upload date YYYY-MM-DD>
Also checks titles are unique across every earlier batch CSV in pins/. Exits 1 on any error."""
import csv, os, re, sys, glob, collections
from datetime import datetime, date
from PIL import Image
path, upload = sys.argv[1], date.fromisoformat(sys.argv[2])
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.reader(open(path, encoding="utf-8"))); hdr, rows = rows[0], rows[1:]
errs = []
if hdr != ["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"]: errs.append(f"header {hdr}")
if len(rows) > 100: errs.append("over 100 rows")
older = set()
for f in glob.glob(os.path.join(REPO, "pins", "*", "*.csv")):
    if os.path.abspath(f) != os.path.abspath(path):
        older |= {r[0] for r in list(csv.reader(open(f, encoding="utf-8")))[1:]}
seen = collections.Counter(r[0] for r in rows)
boards = {"Net Worth Tracker","2027 Planner & Goal Setting","Investment Portfolio Tracker","Small Business Spreadsheets"}
hype = re.compile(r"\b(ultimate|game-?changer|must-have|best|guaranteed|financial freedom)\b", re.I)
day_boards = collections.defaultdict(list)
for t, url, board, thumb, desc, link, pub, kw in rows:
    if seen[t] > 1 or t in older: errs.append(f"title not unique: {t}")
    if not 1 <= len(t) <= 100: errs.append(f"title length {len(t)}")
    if len(desc) > 500: errs.append(f"description length {len(desc)}: {t}")
    if board not in boards: errs.append(f"unknown board {board}")
    if thumb: errs.append("thumbnail not blank")
    if not re.fullmatch(r"https://www\.etsy\.com/listing/\d+/[a-z0-9-]+", link): errs.append(f"link {link}")
    m = re.fullmatch(r"https://lifefreedomstore\.github\.io/lifefreedom-pins/(pins/[^/]+/[^/]+\.png)", url)
    if not m: errs.append(f"media url {url}")
    else:
        f = os.path.join(REPO, m.group(1))
        if not os.path.exists(f): errs.append(f"missing {f}")
        elif Image.open(f).size != (1000, 1500): errs.append(f"size {f}")
    d = datetime.strptime(pub, "%Y-%m-%dT%H:%M:%S").date()
    if not 0 <= (d - upload).days <= 13: errs.append(f"{pub} is {(d - upload).days} days after upload {upload}")
    if hype.search(t + " " + desc): errs.append(f"hype word: {t}")
    day_boards[d].append(board)
for d, b in day_boards.items():
    if len(b) != len(set(b)): errs.append(f"board twice on {d}")
print(f"{len(rows)} rows, {len(day_boards)} days, {min(day_boards)} to {max(day_boards)}")
print("ERRORS:", errs or "none"); sys.exit(1 if errs else 0)

"""Build a Pinterest batch: render pins into the GitHub Pages repo, write the bulk-upload CSV,
a contact sheet per product and an index.html.
Usage (from the repo's tools/ folder): python build_batch.py <batch> <first date YYYY-MM-DD> <days> <specs module>
e.g.  python build_batch.py batch-02 2026-11-20 10 batch02_specs
Needs: fonts/Fraunces.ttf copied to /home/claude/fonts/, Inter in /usr/share/fonts/opentype/inter/."""
import csv, os, sys, html
from datetime import date, timedelta
import importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pinkit import render, contact_sheet
PRODUCTS = importlib.import_module(sys.argv[4] if len(sys.argv) > 4 else "batch01_specs").PRODUCTS

BATCH, START, DAYS = sys.argv[1], date.fromisoformat(sys.argv[2]), int(sys.argv[3])
REPO = os.path.dirname(HERE)
BASE = f"https://lifefreedomstore.github.io/lifefreedom-pins/pins/{BATCH}/"
OUT = os.path.join(REPO, "pins", BATCH)
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
TIMES = ["08:00:00", "12:30:00", "19:30:00", "21:00:00"]

# per product: alternate templates so variants are spread out
order = ["hero", "features", "statement", "closeup", "seasonal"]
queues = {}
for prod, P in PRODUCTS.items():
    by_t = {t: [p for p in P["pins"] if p["template"] == t] for t in order}
    q = [by_t[t][i] for i in range(2) for t in order]
    for n, p in enumerate(q, 1):
        p["file"] = f"{prod}-{p['template']}-{n:02d}.png"
        p["prod"] = prod
    queues[prod] = q

# round-robin across products -> no product twice in a row
seq = []
while any(queues.values()):
    for prod in PRODUCTS:
        if queues[prod]:
            seq.append(queues[prod].pop(0))

per_day = -(-len(seq) // DAYS)
rows, paths, seen = [], {}, {}
for i, p in enumerate(seq):
    day = i * DAYS // len(seq)          # spread evenly: 3 a day, the odd extra early
    slot = seen.get(day, 0); seen[day] = slot + 1
    d = START + timedelta(days=day)
    P = PRODUCTS[p["prod"]]
    path = render(p, os.path.join(OUT, p["file"]))
    paths.setdefault(p["prod"], []).append(path)
    # Pinterest rejects a CSV that repeats a destination link ("Duplicate Pin link"), so every pin
    # gets its own tracked URL; Etsy ignores the extra parameters and the listing opens as normal.
    link = f"{P['link']}?utm_source=pinterest&utm_medium=social&utm_campaign={BATCH}&utm_content={p['file'][:-4]}"
    rows.append([p["title"], BASE + p["file"], P["board"], "", p["desc"], link,
                 f"{d.isoformat()}T{TIMES[slot % len(TIMES)]}", P["kw"]])

csv_path = os.path.join(OUT, f"LifeFreedomStore_pins_{BATCH}.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"])
    w.writerows(rows)
for prod, ps in paths.items():
    contact_sheet(ps, os.path.join(HERE, "out", f"contact-{BATCH}-{prod}.png"), cols=5)

with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(f"<!doctype html><meta charset='utf-8'><title>{BATCH}</title><h1>{BATCH}: {len(rows)} pins</h1><ul>")
    for r in rows:
        f.write(f"<li><a href='{html.escape(r[1])}'>{html.escape(r[1].rsplit('/', 1)[1])}</a> · {r[6]} · {html.escape(r[2])}</li>")
    f.write("</ul>")
print(csv_path, len(rows), "pins,", per_day, "a day")

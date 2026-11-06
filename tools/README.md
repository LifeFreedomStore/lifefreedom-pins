# Pin tooling (LifeFreedomStore)

- `crops.py` cuts real product screens out of the live Etsy listing photos (masters 2576x1932).
- `pinkit.py` holds the 5 approved templates (hero, features, statement, closeup, seasonal), 1000x1500, brand v1.5.
- `batch01_specs.py` holds the copy for each pin (title <=100, description <=500, keyword first, no hype, finance pins carry "not financial advice").
- `build_batch.py <batch> <first publish date> <days>` renders pins into `pins/<batch>/`, writes the Pinterest bulk CSV
  (Title, Media URL, Pinterest board, Thumbnail, Description, Link, Publish date, Keywords) and contact sheets.

Pinterest rules: <=100 rows per CSV, every publish date within 14 days of upload, board names exact, titles unique.

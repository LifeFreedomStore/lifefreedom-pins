# Pin tooling (LifeFreedomStore)

- `crops.py` cuts real product screens out of the live Etsy listing photos (masters 2576x1932).
- `pinkit.py` holds the 5 approved templates (hero, features, statement, closeup, seasonal), 1000x1500, brand v1.5.
- `batch01_specs.py` holds the copy for each pin (title <=100, description <=500, keyword first, no hype, finance pins carry "not financial advice").
- `build_batch.py <batch> <first publish date> <days>` renders pins into `pins/<batch>/`, writes the Pinterest bulk CSV
  (Title, Media URL, Pinterest board, Thumbnail, Description, Link, Publish date, Keywords) and contact sheets.

Pinterest rules: <=100 rows per CSV, every publish date within 14 days of upload, board names exact, titles unique.

## Product registry (from 9 Nov 2026)
`products.json` lists every product, its board, keywords and Etsy link. The Monday run pins only products with `"live": true` and a real `link`.

To add a product:
1. Publish the listing on Etsy.
2. Create its Pinterest board, using the exact name in `products.json`.
3. Set `live` to true and paste the listing URL into `link`.
4. Make sure `screens/<key>/` holds real crops from its listing photos.

`build_batch.py` takes 1 or 2 pins per template per product, so the batch can stay within 40 pins as products are added.

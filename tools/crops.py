"""Crop real product screens out of the live Etsy listing photos (2576x1932 masters; boxes in 2000x1500 units)."""
from PIL import Image
A = "/mnt/user-data/attachments/a1bbf177-bc9b-5b48-9fe8-7b3c2abcdf3a/"
C = {
 "smallbiz": {"dash": ("3e125e02-image.jpg", (466, 563, 1534, 1012)),
              "needs": ("c5850df2-image.jpg", (122, 334, 1878, 772)),
              "pace": ("d67150e7-image.jpg", (122, 334, 1318, 876)),
              "chart": ("d67150e7-image.jpg", (122, 917, 1318, 1358)),
              "dashtop": ("465034d7-image.jpg", (505, 674, 1494, 1066))},
 "planner": {"dash": ("42e76621-image.jpg", (550, 505, 1450, 1005)),
             "checks": ("9f0a481c-image.jpg", (122, 334, 1878, 1138)),
             "weekly": ("dea50247-image.jpg", (122, 348, 1878, 1134))},
 "networth": {"dash": ("e7a931d2-image.jpg", (550, 462, 1450, 1050)),
              "whatif": ("d9741e79-image.jpg", (122, 347, 1878, 701)),
              "whatifchart": ("d9741e79-image.jpg", (122, 794, 1158, 1148)),
              "bills": ("c6b9e778-image.jpg", (122, 348, 1384, 1296))},
}
import os
for prod, d in C.items():
    os.makedirs(f"screens/{prod}", exist_ok=True)
    for name, (f, box) in d.items():
        im = Image.open(A + f).convert("RGB")
        s = im.width / 2000
        im.crop(tuple(round(v * s) for v in box)).save(f"screens/{prod}/{name}.png")
# preview sheet
ims = [Image.open(f"screens/{p}/{n}.png") for p, d in C.items() for n in d]
th = []
for i in ims:
    i = i.copy(); i.thumbnail((520, 360)); th.append(i)
W = 3 * 540 + 20; rows = (len(th) + 2) // 3
sheet = Image.new("RGB", (W, rows * 380 + 20), (200, 60, 60))
for k, i in enumerate(th):
    sheet.paste(i, (20 + (k % 3) * 540, 20 + (k // 3) * 380))
sheet.save("/home/claude/pins/_crops.png")
print(len(ims))

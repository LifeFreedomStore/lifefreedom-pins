"""LifeFreedomStore Pinterest pin templates (brand v1.5: Ink/Paper/Teal, Fraunces + Inter).
Pins are 1000 x 1500 (2:3). Five templates, one function each, all driven by a spec dict:
  hero      bold Ink background, tag pill, product name, device mockup, format badge
  features  Paper background, headline, screen card, 4 ticked benefit lines
  statement bold one-line statement (no questions here; use 'bold' for question hooks), screen below
  closeup   zoomed crop of one real screen + one big callout from that render
  seasonal  timely frame (e.g. new year reset) around the hero screen
  bold      in-your-face hook: full-bleed Ink or Teal, a huge question or claim in Fraunces, a Teal answer
            line, a real screen, a CTA bar (added 9 Nov 2026 at Matt's request for the bookkeeping tracker;
            question hooks are allowed here only, kept huge so they read at feed size)
Screens are real renders of the built workbooks (each asset's media/render_sheets.py).
Rules: keyword in the overlay, nothing in the top-right 220 x 220 corner, 60 px side margins,
headline >= 60 px, wordmark bottom-right, no prices, UK English."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

Image.MAX_IMAGE_PIXELS = None
W, H, M = 1000, 1500, 60
INK, PAPER, SLATE, TEAL, DTEAL, TINT, MIST, WHITE = (
    (31, 42, 68), (250, 247, 242), (91, 100, 114), (0, 163, 137), (0, 112, 94), (210, 241, 235),
    (221, 227, 232), (255, 255, 255))
FRAUNCES = "/home/claude/fonts/Fraunces.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"


def fr(size):
    return ImageFont.truetype(FRAUNCES, size)


def it(size, weight="Regular"):
    return ImageFont.truetype(INTER.format(weight), size)


# ---------- text ----------
def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, maker, width, start, minimum, max_lines):
    """Largest size (>= minimum) at which text wraps into <= max_lines within width."""
    size = start
    while size >= minimum:
        f = maker(size)
        lines = wrap(d, text, f, width)
        if len(lines) <= max_lines and all(d.textlength(l, font=f) <= width for l in lines):
            return f, size, lines
        size -= 4
    raise ValueError(f"text does not fit: {text!r}")


def headline(d, x, y, text, accent, colour, width, start=110, minimum=60, max_lines=3, gap=1.08, centre=False):
    """Fraunces headline; words in `accent` (a phrase) drawn in Teal. Returns y after the block."""
    f, size, lines = fit_lines(d, text, fr, width, start, minimum, max_lines)
    acc = set(accent.lower().split()) if accent else set()
    for line in lines:
        words = line.split(" ")
        lw = d.textlength(line, font=f)
        cx = x + (width - lw) / 2 if centre else x
        for i, wd in enumerate(words):
            t = wd + (" " if i < len(words) - 1 else "")
            col = TEAL if wd.lower().strip(".,:") in acc else colour
            d.text((cx, y), t, font=f, fill=col)
            cx += d.textlength(t, font=f)
        y += int(size * gap)
    return y


def pill(d, x, y, text, size=30, bg=DTEAL, fg=WHITE, pad=(28, 14), centre=False):
    f = it(size, "SemiBold")
    w = d.textlength(text, font=f) + 2 * pad[0]
    h = size + 2 * pad[1]
    if centre:
        x = x - w / 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    d.text((x + pad[0], y + h / 2), text, font=f, fill=fg, anchor="lm")
    return x + w, y + h


def wordmark(im, right, base, size=34, ink=INK, slate=SLATE):
    d = ImageDraw.Draw(im)
    fa, fb = fr(size), it(int(size * 0.6), "Medium")
    wa, wb = d.textlength("LifeFreedom", font=fa), d.textlength("Store", font=fb)
    x0 = right - wa - 4 - wb
    d.text((x0, base), "LifeFreedom", font=fa, fill=ink, anchor="ls")
    d.text((x0 + wa + 4, base), "Store", font=fb, fill=slate, anchor="ls")


# ---------- images ----------
def fit(src, w=None, h=None):
    if w and not h:
        h = round(src.height * w / src.width)
    elif h and not w:
        w = round(src.width * h / src.height)
    return src.resize((max(1, w), max(1, h)), Image.LANCZOS)


def cover(src, w, h, anchor=(0.5, 0.0)):
    """Scale src to fill w x h, crop around anchor (fractions)."""
    s = max(w / src.width, h / src.height)
    r = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
    x = round((r.width - w) * anchor[0])
    y = round((r.height - h) * anchor[1])
    return r.crop((x, y, x + w, y + h))


def shadow(im, box, radius=20, blur=18, offset=(0, 12), alpha=60):
    x0, y0, x1, y1 = box
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]], radius=radius, fill=alpha)
    im.paste(Image.new("RGB", im.size, (12, 16, 28)), (0, 0), m.filter(ImageFilter.GaussianBlur(blur)))


def rounded_paste(im, src, xy, radius):
    m = Image.new("L", src.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, src.width - 1, src.height - 1], radius=radius, fill=255)
    im.paste(src, xy, m)


def card(im, src, x, y, w, h, radius=18, border=MIST, anchor=(0.5, 0.0), dark=False):
    h = min(h, round(w * src.height / src.width))
    s = cover(src, w, h, anchor)
    shadow(im, (x, y, x + w, y + h), radius=radius, alpha=110 if dark else 60)
    ImageDraw.Draw(im).rounded_rectangle([x - 3, y - 3, x + w + 3, y + h + 3], radius=radius + 3, fill=border)
    rounded_paste(im, s, (x, y), radius)
    return (x, y, x + w, y + h)


def device(im, screen, x, y, w, h_screen, anchor=(0.5, 0.0), dark=False):
    """Original, unbranded monitor: Ink bezel (Slate edge on dark backgrounds), Slate neck and base."""
    b = max(10, int(w * 0.024))
    sw = w - 2 * b
    sh = min(h_screen, round(sw * screen.height / screen.width))
    scr = cover(screen, sw, sh, anchor)
    h = sh + 2 * b
    neck_w, neck_h, base_w, base_h = int(w * 0.11), int(w * 0.07), int(w * 0.36), int(w * 0.02)
    shadow(im, (x + 20, y + 14, x + w - 20, y + h), radius=b * 2, blur=26, offset=(0, 20), alpha=120 if dark else 50)
    d = ImageDraw.Draw(im)
    cx = x + w / 2
    d.polygon([(cx - neck_w * 0.42, y + h - 4), (cx + neck_w * 0.42, y + h - 4),
               (cx + neck_w / 2, y + h + neck_h), (cx - neck_w / 2, y + h + neck_h)], fill=SLATE)
    d.rounded_rectangle([cx - base_w / 2, y + h + neck_h - 2, cx + base_w / 2, y + h + neck_h + base_h],
                        radius=base_h // 2, fill=SLATE)
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(b * 1.6), fill=INK, outline=SLATE if dark else None,
                        width=3 if dark else 0)
    rounded_paste(im, scr, (x + b, y + b), 6)
    return (x, y, x + w, y + h + neck_h + base_h)


def tick(d, x, y, size=44):
    d.ellipse([x, y, x + size, y + size], fill=TEAL)
    s = size / 44
    d.line([(x + 12 * s, y + 23 * s), (x + 19 * s, y + 30 * s), (x + 32 * s, y + 15 * s)], fill=WHITE, width=max(3, int(5 * s)), joint="curve")


def screen(path):
    return Image.open(path).convert("RGB")


# ---------- templates ----------
def t_hero(spec):
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    pill(d, M, 70, spec["tag"], size=28, bg=TEAL, fg=INK)
    y = headline(d, M, 150, spec["title_overlay"], spec.get("accent", ""), PAPER, W - 2 * M, start=104, max_lines=3)
    d.text((M, y + 20), spec["sub"], font=it(34, "Medium"), fill=MIST)
    top = y + 110
    device(im, screen(spec["screen"]), M, top, W - 2 * M, int((W - 2 * M) * 0.64), spec.get("anchor", (0.5, 0.0)), dark=True)
    pill(d, W / 2, H - 200, spec.get("badge", "Google Sheets + Excel"), size=32, centre=True)
    d.text((W / 2, H - 112), spec.get("footer", "Instant download"), font=it(28, "Medium"), fill=MIST, anchor="mm")
    wordmark(im, W - M, H - 44, ink=PAPER, slate=MIST)
    return im


def t_features(spec):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.text((M, 78), spec["kicker"].upper(), font=it(28, "SemiBold"), fill=DTEAL)
    y = headline(d, M, 124, spec["title_overlay"], spec.get("accent", ""), INK, W - 2 * M, start=92, max_lines=3)
    src = screen(spec["screen"])
    ch = min(520, round((W - 2 * M) * src.height / src.width)) if spec.get("fit") else 520
    card(im, src, M, y + 44, W - 2 * M, ch, anchor=spec.get("anchor", (0.5, 0.0)))
    y += 44 + ch + 56
    f = it(38, "Medium")
    for line in spec["bullets"][:4]:
        tick(d, M, y)
        d.text((M + 66, y + 22), line, font=f, fill=INK, anchor="lm")
        y += 78
    pill(d, M, H - 112, spec.get("badge", "Google Sheets + Excel"), size=28)
    wordmark(im, W - M, H - 66)
    return im


def t_statement(spec):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 640], fill=TEAL)
    y = headline(d, M, 110, spec["statement"], "", INK, W - 2 * M, start=120, minimum=72, max_lines=3, gap=1.04)
    d.text((M, y + 44), spec["sub"], font=it(36, "SemiBold"), fill=INK)
    card(im, screen(spec["screen"]), M, 700, W - 2 * M, 560, anchor=spec.get("anchor", (0.5, 0.0)))
    d.text((M, H - 150), spec["product"], font=fr(44), fill=INK)
    d.text((M, H - 92), spec.get("badge", "Google Sheets + Excel"), font=it(28, "Medium"), fill=SLATE)
    wordmark(im, W - M, H - 66)
    return im


def t_closeup(spec):
    """Real screen on top, Ink callout with one example number, headline + sub; stacked and centred
    so nothing collides with the footnote whatever the screen shape or headline length."""
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    src = screen(spec["screen"])
    if spec.get("crop"):
        l, t, r, b = spec["crop"]
        src = src.crop((round(l * src.width), round(t * src.height), round(r * src.width), round(b * src.height)))
    ih = min(760, round(W * src.height / src.width))
    hf, hsize, hlines = fit_lines(d, spec["title_overlay"], fr, W - 2 * M, 76, 60, 2)
    head_h = len(hlines) * int(hsize * 1.08)
    block = ih + 40 + 230 + 48 + head_h + 20 + 40          # image, gap, callout, gap, headline, gap, sub
    limit = H - 140                                         # footnote + wordmark zone starts here
    top = max(0, (limit - block) // 2) if ih < 760 else 0
    card(im, src, 0, top, W, ih, radius=0, border=PAPER, anchor=spec.get("anchor", (0.5, 0.0)))
    box_y = top + ih + 40
    d.rounded_rectangle([M, box_y, W - M, box_y + 230], radius=26, fill=INK)
    d.text((M + 44, box_y + 40), spec["callout_label"], font=it(32, "SemiBold"), fill=MIST)
    d.text((M + 44, box_y + 92), spec["callout_value"], font=it(96, "Bold"), fill=TEAL)
    y = headline(d, M, box_y + 230 + 48, spec["title_overlay"], spec.get("accent", ""), INK, W - 2 * M, start=76, max_lines=2)
    sub_y = y + 20
    assert sub_y + 40 <= limit, ("closeup overflow", spec["title_overlay"])
    d.text((M, sub_y), spec["sub"], font=it(32, "Medium"), fill=SLATE)
    d.text((M, H - 92), spec.get("note", "Example data shown"), font=it(24), fill=SLATE)
    wordmark(im, W - M, H - 66)
    return im


def t_seasonal(spec):
    im = Image.new("RGB", (W, H), TINT)
    d = ImageDraw.Draw(im)
    d.text((W / 2, 175), spec["big"], font=fr(230), fill=INK, anchor="mm")
    y = headline(d, M, 320, spec["title_overlay"], spec.get("accent", ""), INK, W - 2 * M, start=86, max_lines=2, centre=True)
    d.text((W / 2, y + 52), spec["sub"], font=it(34, "Medium"), fill=SLATE, anchor="mm")
    device(im, screen(spec["screen"]), M + 20, y + 120, W - 2 * M - 40, int((W - 2 * M - 40) * 0.6), spec.get("anchor", (0.5, 0.0)))
    pill(d, W / 2, H - 230, spec["product"], size=32, bg=INK, fg=PAPER, centre=True)
    d.text((W / 2, H - 140), spec.get("badge", "Google Sheets + Excel · Instant download"), font=it(28, "Medium"), fill=INK, anchor="mm")
    wordmark(im, W - M, H - 50)
    return im


def t_bold(spec):
    """Big hook. spec: hook (question or claim), accent (phrase in Teal/Paper), answer, screen, cta,
    bg ('ink' default or 'teal'), optional anchor/crop."""
    teal_bg = spec.get("bg", "ink") == "teal"
    bg, fg = (TEAL, INK) if teal_bg else (INK, PAPER)
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    if spec.get("tag"):
        pill(d, M, 64, spec["tag"], size=28, bg=(INK if teal_bg else TEAL), fg=(PAPER if teal_bg else INK))
    y = 150
    # huge hook: up to 4 lines, never below 92 px
    f, size, lines = fit_lines(d, spec["hook"], fr, W - 2 * M, 150, 92, 4)
    acc = {w.strip(".,:?!") for w in spec.get("accent", "").lower().split()}
    acc_col = PAPER if teal_bg else TEAL
    for line in lines:
        cx = M
        words = line.split(" ")
        for i, wd in enumerate(words):
            t = wd + (" " if i < len(words) - 1 else "")
            d.text((cx, y), t, font=f, fill=acc_col if wd.lower().strip(".,:?!") in acc else fg)
            cx += d.textlength(t, font=f)
        y += int(size * 1.02)
    y += 28
    # answer line in a contrasting bar
    af = it(40, "Bold")
    aw = d.textlength(spec["answer"], font=af)
    assert aw <= W - 2 * M - 56, ("bold answer too long", spec["answer"])
    d.rounded_rectangle([M, y, M + aw + 56, y + 84], radius=42, fill=(INK if teal_bg else TEAL))
    d.text((M + 28, y + 42), spec["answer"], font=af, fill=(PAPER if teal_bg else INK), anchor="lm")
    top = y + 84 + 44
    src = screen(spec["screen"])
    if spec.get("crop"):
        l, t, r, b = spec["crop"]
        src = src.crop((round(l * src.width), round(t * src.height), round(r * src.width), round(b * src.height)))
    sh = H - 230 - top
    assert sh >= 300, ("bold: hook too tall for the screen", spec["hook"])
    card(im, src, M, top, W - 2 * M, sh, anchor=spec.get("anchor", (0.5, 0.0)), dark=not teal_bg)
    d.text((M, H - 150), spec["cta"], font=it(36, "Bold"), fill=fg)
    d.text((M, H - 100), spec.get("badge", "Google Sheets + Excel · Instant download"), font=it(28, "Medium"),
           fill=(INK if teal_bg else MIST))
    wordmark(im, W - M, H - 44, ink=fg, slate=(INK if teal_bg else MIST))
    return im


TEMPLATES = {"hero": t_hero, "features": t_features, "statement": t_statement, "closeup": t_closeup, "seasonal": t_seasonal, "bold": t_bold}


def render(spec, out):
    im = TEMPLATES[spec["template"]](spec)
    assert im.size == (W, H)
    im.save(out, "PNG", optimize=True)
    return out


def contact_sheet(paths, out, cols=5, thumb=300):
    ims = [Image.open(p) for p in paths]
    th = int(thumb * 1.5)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb + 24) + 24, rows * (th + 24) + 24), MIST)
    for i, img in enumerate(ims):
        x, y = 24 + (i % cols) * (thumb + 24), 24 + (i // cols) * (th + 24)
        sheet.paste(img.resize((thumb, th), Image.LANCZOS), (x, y))
    sheet.save(out, "PNG", optimize=True)
    return out

#!/usr/bin/env python3
"""Build SATA_prezentatsia.pptx from presentation.html.

The HTML stays the single source. Every slide becomes a PowerPoint slide with
  * a native title bar, footer and slide number (real text, Arial),
  * the slide body as a 2x picture rendered by headless Chrome, so diagrams,
    tables and Cyrillic text look the same on any machine and need no fonts,
  * the slide text in the speaker notes (searchable, accessible).

Elements marked data-step="N" in the HTML are left out of the body picture and
added as separate pictures with a native PowerPoint entrance animation
(data-fx="wipe" or "fade"), one mouse click per step.

Needs python-pptx (which brings Pillow):

  python3 -m venv ~/venvs/tu-kp && ~/venvs/tu-kp/bin/pip install python-pptx
  ~/venvs/tu-kp/bin/python III-kurs/KP/SATA/src/build_pptx.py
"""
import html
import io
import re
import subprocess
import tempfile
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1280, 720          # slide size in CSS px (13.333in x 7.5in)
SCALE = 2                 # render scale
PX = 9525                 # EMU per CSS px
TILES = 6                 # slide variants per Chrome screenshot
FOOTER = "SATA – Компютърна периферия"
NAVY, ORANGE, GREY = RGBColor(0x0B, 0x3D, 0x63), RGBColor(0xF2, 0x8C, 0x28), RGBColor(0x64, 0x74, 0x8B)
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"

BASE_CSS = """
html, body { background: transparent !important }
.slide { counter-increment: none !important; page-break-after: auto !important }
.slide * { animation: none !important }
.cursor { display: none !important }
.tile { width: 1280px; height: 720px; overflow: hidden }
.tile:not(.full) .slide > h2 { visibility: hidden }
.tile:not(.full) .slide::before, .tile:not(.full) .slide::after { display: none }
.v-step .slide { background: transparent !important }
"""

# Decides, element by element, what a tile shows: the base tile everything that is not
# part of a step, a step tile only the elements whose nearest data-step ancestor is that step.
LAYER_JS = """<script>
document.querySelectorAll('.tile').forEach(t => {
  const v = t.dataset.v, k = t.dataset.k;
  if (v === 'full') return;
  t.querySelectorAll('.slide *').forEach(e => {
    if (e.closest('defs')) { e.style.setProperty('visibility', 'visible', 'important'); return; }
    if (v === 'base' && e.matches('h2, h2 *')) return;
    const c = e.closest('[data-step]');
    const show = v === 'base' ? !c : (c && c.dataset.step === k);
    e.style.setProperty('visibility', show ? 'visible' : 'hidden', 'important');
  });
});
</script>"""


def render_tiles(head, tiles, tmp):
    """tiles: list of (css_class, slide_html, number, step). Returns RGBA images, one per tile."""
    images = []
    for start in range(0, len(tiles), TILES):
        batch = tiles[start:start + TILES]
        css, body = BASE_CSS, ""
        for i, (cls, slide, number, step) in enumerate(batch):
            variant = {"full": "full", "v-base": "base", "v-step": "step"}[cls]
            body += (f'<div class="tile {cls}" data-v="{variant}" data-k="{step}" '
                     f'style="counter-reset: s {number}">{slide}</div>')
        page = SRC / ".pptx.html"
        page.write_text(head.replace("</head>", f"<style>{css}</style></head>") + f"<body>{body}{LAYER_JS}</body></html>",
                        encoding="utf-8")
        shot = tmp / "shot.png"
        try:
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--default-background-color=00000000", f"--force-device-scale-factor={SCALE}",
                            f"--window-size={W},{H * len(batch)}", f"--screenshot={shot}", page.as_uri()],
                           check=True, capture_output=True)
        finally:
            page.unlink()
        sheet = Image.open(shot).convert("RGBA")
        for i in range(len(batch)):
            images.append(sheet.crop((0, i * H * SCALE, W * SCALE, (i + 1) * H * SCALE)))
    return images


def plain_text(fragment):
    fragment = re.sub(r"<(svg|style)\b.*?</\1>", " ", fragment, flags=re.S)
    fragment = re.sub(r"</(li|p|tr|h1|h2|div|figcaption)>", "\n", fragment)
    text = html.unescape(re.sub(r"<[^>]+>", " ", fragment))
    lines = [" ".join(line.split()) for line in text.split("\n")]
    return "\n".join(line for line in lines if line)


def add_text(slide, x, y, w, h, runs, align=PP_ALIGN.LEFT):
    """runs: list of (text, size_pt, bold, RGBColor)."""
    box = slide.shapes.add_textbox(Emu(x * PX), Emu(y * PX), Emu(w * PX), Emu(h * PX))
    frame = box.text_frame
    frame.word_wrap = False
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    para = frame.paragraphs[0]
    para.alignment = align
    for text, size, bold, color in runs:
        run = para.add_run()
        run.text = text
        run.font.name = "Arial"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run._r.get_or_add_rPr().set("lang", "bg-BG")
    return box


def add_rect(slide, x, y, w, h, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(x * PX), Emu(y * PX), Emu(w * PX), Emu(h * PX))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def add_picture(slide, image, x, y, tmp, name, opaque):
    """x, y in CSS px; image is at SCALE. Opaque pictures may be stored as JPEG when PNG is large."""
    path = tmp / f"{name}.png"
    if opaque:
        image = image.convert("RGB")
    image.save(path, optimize=True)
    if opaque and path.stat().st_size > 900_000:
        path = tmp / f"{name}.jpg"
        image.save(path, quality=90)
    return slide.shapes.add_picture(str(path), Emu(round(x * PX)), Emu(round(y * PX)),
                                    Emu(round(image.width / SCALE * PX)), Emu(round(image.height / SCALE * PX)))


def effect(node_id, shape_id, fx, first):
    """One click-triggered entrance effect (Wipe from left or Fade) as PowerPoint timing XML."""
    preset, subtype, flt, dur = (22, 8, "wipe(left)", 1500) if fx == "wipe" else (10, 0, "fade", 600)
    return f'''<p:par xmlns:p="{P_NS}"><p:cTn id="{node_id}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>
<p:par><p:cTn id="{node_id + 1}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
<p:par><p:cTn id="{node_id + 2}" presetID="{preset}" presetClass="entr" presetSubtype="{subtype}" fill="hold" grpId="0" nodeType="clickEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
<p:set><p:cBhvr><p:cTn id="{node_id + 3}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{shape_id}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
<p:animEffect transition="in" filter="{flt}"><p:cBhvr><p:cTn id="{node_id + 4}" dur="{dur}"/><p:tgtEl><p:spTgt spid="{shape_id}"/></p:tgtEl></p:cBhvr></p:animEffect>
</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'''


def add_timing(slide, steps):
    """steps: list of (shape_id, fx) in click order."""
    effects = "".join(effect(3 + 5 * i, sid, fx, i == 0) for i, (sid, fx) in enumerate(steps))
    xml = f'''<p:timing xmlns:p="{P_NS}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>
<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{effects}</p:childTnLst></p:cTn>
<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>
</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'''
    slide._element.append(etree.fromstring(xml))


def header_height(image):
    """Height (CSS px) of the navy bar + orange rule, read from a fully rendered slide."""
    pixels = image.convert("RGB")
    y = 0
    while pixels.getpixel((20, y)) != (255, 255, 255):
        y += 1
    return y / SCALE


def main():
    source = (SRC / "presentation.html").read_text(encoding="utf-8")
    head = source[:source.index("<body>")]
    slides = re.findall(r'<section class="slide.*?</section>', source, re.S)
    total = len(slides)

    tiles, plan = [], []
    for number, slide in enumerate(slides, 1):
        full = bool(re.match(r'<section class="slide (title|end)"', slide))
        steps = sorted({int(s) for s in re.findall(r'data-step="(\d+)"', slide)})
        entry = {"number": number, "full": full, "html": slide, "base": len(tiles), "steps": []}
        tiles.append(("full" if full else "v-base", slide, number, None))
        for step in steps:
            fx = re.search(rf'data-step="{step}" data-fx="(\w+)"', slide)[1]
            entry["steps"].append((len(tiles), fx))
            tiles.append(("v-step", slide, number, step))
        plan.append(entry)
    probe = len(tiles)
    tiles.append(("full", slides[2], 3, None))

    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(W * PX), Emu(H * PX)
    prs.core_properties.title = "SATA (Serial ATA) – архитектура, протокол и приложение"
    prs.core_properties.author = "Алекс Огнянов, Йордан Начев, Магдалена Джисова"
    prs.core_properties.language = "bg-BG"
    blank = prs.slide_layouts[6]

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        images = render_tiles(head, tiles, tmp)
        bar = header_height(images[probe])
        animated = 0
        for entry in plan:
            n, slide = entry["number"], prs.slides.add_slide(blank)
            base = images[entry["base"]]
            notes = plain_text(entry["html"])
            if entry["full"]:
                pic = add_picture(slide, base, 0, 0, tmp, f"s{n}", opaque=True)
            else:
                body = base.crop((0, round(bar * SCALE), W * SCALE, H * SCALE))
                pic = add_picture(slide, body, 0, bar, tmp, f"s{n}", opaque=True)
                add_rect(slide, 0, 0, W, bar - 6, NAVY)
                add_rect(slide, 0, bar - 6, W, 6, ORANGE)
                m = re.search(r"<h2>(.*?)</h2>", entry["html"], re.S)
                small = re.search(r"<small>(.*?)</small>", m[1], re.S)
                title = html.unescape(re.sub(r"<small>.*?</small>|<[^>]+>", "", m[1], flags=re.S)).strip()
                runs = [(title, 25.5, True, RGBColor(0xFF, 0xFF, 0xFF))]
                if small:
                    runs.append(("   " + html.unescape(re.sub(r"<[^>]+>", "", small[1])).strip(), 15, False,
                                 RGBColor(0xBC, 0xD4, 0xEA)))
                add_text(slide, 48, 0, W - 96, bar - 6, runs)
                add_text(slide, 48, 688, 600, 22, [(FOOTER, 11.25, False, GREY)])
                add_text(slide, W - 48 - 200, 688, 200, 22, [(f"{n} / {total}", 11.25, True, GREY)], PP_ALIGN.RIGHT)
            pic._element.nvPicPr.cNvPr.set("descr", notes[:2000])
            slide.notes_slide.notes_text_frame.text = notes
            timing = []
            for k, (index, fx) in enumerate(entry["steps"], 1):
                layer = images[index]
                box = layer.getchannel("A").getbbox()
                if box is None:
                    raise SystemExit(f"slide {n}: step {k} rendered empty")
                pad = 2 * SCALE
                box = (max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, W * SCALE), min(box[3] + pad, H * SCALE))
                shape = add_picture(slide, layer.crop(box), box[0] / SCALE, box[1] / SCALE, tmp, f"s{n}k{k}", opaque=False)
                shape.name = f"Стъпка {k}"
                timing.append((shape.shape_id, fx))
            if timing:
                add_timing(slide, timing)
                animated += 1
        final = OUT / "SATA_prezentatsia.pptx"
        prs.save(final)
    print(f"{final.relative_to(OUT.parent.parent.parent)}: {total} slides, {animated} animated, "
          f"{final.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()

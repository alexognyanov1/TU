#!/usr/bin/env python3
"""Render the SATA реферат and presentation to PDF with headless Chrome.

The реферат is rendered twice: the first pass finds the page of every heading,
the second fills those page numbers into the table of contents. The second pass
is written next to the source so relative assets (the TU logo) still resolve.

With --video the animated diagrams of the presentation (slides 16-18, CSS
animations that play when the HTML is opened in a browser) are also rendered to
SATA_animatsiya.mp4: every frame is the slide with its animations paused at a
given time, screenshot by headless Chrome and joined by ffmpeg.

  python3 III-kurs/KP/SATA/src/build.py [--video]
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def render(html_path, pdf_path):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                   check=True, capture_output=True)


def page_texts(pdf_path):
    text = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"],
                          check=True, capture_output=True, text=True).stdout
    return [" ".join(p.split()).upper() for p in text.split("\f")]


def build_referat():
    source = (SRC / "referat.html").read_text(encoding="utf-8")
    headings = {hid: " ".join(html.unescape(re.sub(r"<[^>]+>", "", t)).split()).upper()
                for hid, t in re.findall(r'<h[12] id="([^"]+)">(.*?)</h[12]>', source)}
    final = OUT / "SATA_referat.pdf"
    with tempfile.TemporaryDirectory() as tmp:
        first = Path(tmp) / "pass1.pdf"
        render(SRC / "referat.html", first)
        pages = page_texts(first)
        toc_page = next(i for i, p in enumerate(pages) if "СЪДЪРЖАНИЕ" in p)
        numbers = {}
        for hid, title in headings.items():
            if hid == "toc":
                continue
            hit = next((i for i in range(toc_page + 1, len(pages)) if title in pages[i]), None)
            if hit is None:
                sys.exit(f"heading not found in PDF: {title}")
            numbers[hid] = hit + 1
        filled = re.sub(r'<span class="pg" data-for="([^"]+)"></span>',
                        lambda m: f'<span class="pg" data-for="{m[1]}">{numbers[m[1]]}</span>', source)
        second = SRC / ".referat.filled.html"
        second.write_text(filled, encoding="utf-8")
        try:
            render(second, final)
        finally:
            second.unlink()
    print(f"{final.relative_to(OUT.parent.parent.parent)}: {len(page_texts(final)) - 1} pages")


VIDEO_SLIDES = (16, 17, 18)
VIDEO_SECONDS = 8
FPS = 25
BATCH = 10


def build_video():
    source = (SRC / "presentation.html").read_text(encoding="utf-8")
    head = source[:source.index("<body>")]
    slides = re.findall(r'<section class="slide.*?</section>', source, re.S)
    freeze = ("<style>.slide { counter-increment: none } "
              ".slide * { animation-play-state: paused !important; "
              "animation-delay: calc(var(--t) * -1s) !important }</style>")
    final = OUT / "SATA_animatsiya.mp4"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        n = 0
        for number in VIDEO_SLIDES:
            slide = slides[number - 1]
            times = [i / FPS for i in range(VIDEO_SECONDS * FPS)]
            for start in range(0, len(times), BATCH):
                batch = times[start:start + BATCH]
                body = "".join(slide.replace('<section class="slide', f'<section style="--t:{t:.3f}; counter-reset: s {number}" class="slide', 1)
                               for t in batch)
                page = SRC / ".frames.html"
                page.write_text(head.replace("</head>", freeze + "</head>") + f"<body>{body}</body></html>", encoding="utf-8")
                shot = tmp / "shot.png"
                try:
                    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                                    "--force-device-scale-factor=1.5", f"--window-size=1280,{720 * len(batch)}",
                                    f"--screenshot={shot}", page.as_uri()], check=True, capture_output=True)
                finally:
                    page.unlink()
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(shot), "-vf", f"untile=1x{len(batch)}",
                                "-start_number", str(n), str(tmp / "f%05d.png")], check=True)
                n += len(batch)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "f%05d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", str(final)],
                       check=True)
    print(f"{final.relative_to(OUT.parent.parent.parent)}: {n / FPS:.0f} s")


def build_presentation():
    final = OUT / "SATA_prezentatsia.pdf"
    render(SRC / "presentation.html", final)
    print(f"{final.relative_to(OUT.parent.parent.parent)}: {len(page_texts(final)) - 1} pages")


if __name__ == "__main__":
    build_referat()
    if (SRC / "presentation.html").exists():
        build_presentation()
    if "--video" in sys.argv[1:]:
        build_video()

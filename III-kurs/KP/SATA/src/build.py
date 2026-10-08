#!/usr/bin/env python3
"""Render the SATA реферат and presentation to PDF with headless Chrome.

The реферат is rendered twice: the first pass finds the page of every heading,
the second fills those page numbers into the table of contents.

  python3 III-kurs/KP/SATA/src/build.py
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
    return [" ".join(p.split()) for p in text.split("\f")]


def build_referat():
    source = (SRC / "referat.html").read_text(encoding="utf-8")
    headings = {hid: " ".join(html.unescape(re.sub(r"<[^>]+>", "", t)).split())
                for hid, t in re.findall(r'<h[12] id="([^"]+)">(.*?)</h[12]>', source)}
    final = OUT / "SATA_referat.pdf"
    with tempfile.TemporaryDirectory() as tmp:
        first = Path(tmp) / "pass1.pdf"
        render(SRC / "referat.html", first)
        pages = page_texts(first)
        toc_page = next(i for i, p in enumerate(pages) if "Съдържание" in p)
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
        second = Path(tmp) / "referat.html"
        second.write_text(filled, encoding="utf-8")
        render(second, final)
    print(f"{final.relative_to(OUT.parent.parent.parent)}: {len(page_texts(final)) - 1} pages")


def build_presentation():
    final = OUT / "SATA_prezentatsia.pdf"
    render(SRC / "presentation.html", final)
    print(f"{final.relative_to(OUT.parent.parent.parent)}: {len(page_texts(final)) - 1} pages")


if __name__ == "__main__":
    build_referat()
    if (SRC / "presentation.html").exists():
        build_presentation()

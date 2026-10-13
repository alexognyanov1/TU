#!/usr/bin/env python3
"""Render the CPU scheduling реферат to PDF with headless Chrome.

Gantt charts, result tables and the quantum chart are generated from sim.py and
inserted at the <!--@...--> markers in referat.html, so every number in the text
comes from the simulator. Then the document is rendered twice: the first pass finds
the page of every heading, the second fills those page numbers into the contents.

  python3 III-kurs/OS/KP/src/build.py
"""
import html
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import sim

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
FINAL = OUT / "OS_121224052_AlexOgnyanov.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def num(x, digits=2):
    return f"{x:.{digits}f}".replace(".", ",")


def gantt_svg(res):
    end = res.length
    width, left, top, bar = 640, 6, 4, 30
    unit = (width - 2 * left) / end
    out = [f'<svg viewBox="0 0 {width} {top + bar + 22}" width="{width}" xmlns="http://www.w3.org/2000/svg" '
           'font-family="Times New Roman, serif" font-size="13">']
    ticks = {0}
    for name, s, e in res.gantt:
        x, w = left + s * unit, (e - s) * unit
        fill = "#d0d0d0" if name in (None, "CS") else "#fff"
        out.append(f'<rect x="{x:.1f}" y="{top}" width="{w:.1f}" height="{bar}" fill="{fill}" stroke="#000" stroke-width="1"/>')
        if name and w >= 14:
            out.append(f'<text x="{x + w / 2:.1f}" y="{top + bar / 2 + 4.5}" text-anchor="middle">{name}</text>')
        ticks.add(e)
    for t in sorted(ticks):
        out.append(f'<text x="{left + t * unit:.1f}" y="{top + bar + 16}" text-anchor="middle" font-size="11">{t}</text>')
    out.append("</svg>")
    return "".join(out)


def figure(svg, caption):
    return f'<figure>{svg}</figure>\n<p class="cap">{caption}</p>'


def table(head, rows, cls="num"):
    h = "".join(f"<th>{c}</th>" for c in head)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><tr>{h}</tr>{body}</table>'


def example_input():
    rows = [(p.name, p.arrival, p.burst, p.priority) for p in sim.EXAMPLE]
    return table(["Процес", "Момент на пристигане", "CPU burst", "Приоритет"], rows)


def process_table(res):
    rows = [(p.name, p.arrival, p.burst, res.completion[p.name], res.turnaround(p), res.waiting(p), res.response(p))
            for p in res.procs]
    rows.append(("<b>Средно</b>", "", "", "", f"<b>{num(res.avg('turnaround'))}</b>",
                 f"<b>{num(res.avg('waiting'))}</b>", f"<b>{num(res.avg('response'))}</b>"))
    return table(["Процес", "Пристигане", "Burst", "Край", "Обработка", "Чакане", "Отговор"], rows)


def example_runs():
    return {alg: res for alg, q, res in sim.runs(sim.EXAMPLE, sim.EXAMPLE_QUANTUM) if alg != "prio-a"}


def summary_example(runs):
    rows = [(sim.label(alg, sim.EXAMPLE_QUANTUM if alg == "rr" else None), num(r.avg("turnaround")),
             num(r.avg("waiting")), num(r.avg("response")), r.switches) for alg, r in runs.items()]
    return table(["Алгоритъм", "Ср. време за обработка", "Ср. време за чакане", "Ср. време за отговор",
                  "Превключвания"], rows, "num first")


def summary_workload(load):
    rows = []
    for alg, q, r in sim.runs(load, 4):
        rows.append((sim.label(alg, q), num(r.avg("turnaround"), 1), num(r.avg("waiting"), 1),
                     num(r.avg("response"), 1), r.worst("waiting"), r.switches))
        if alg == "rr":
            r = sim.simulate(load, "rr", 20)
            rows.append((sim.label("rr", 20), num(r.avg("turnaround"), 1), num(r.avg("waiting"), 1),
                         num(r.avg("response"), 1), r.worst("waiting"), r.switches))
    return table(["Алгоритъм", "Ср. обработка", "Ср. чакане", "Ср. отговор", "Макс. чакане", "Превключвания"],
                 rows, "num first")


def quantum_table(sweep):
    rows = [(q, num(tat, 1), num(resp, 1), sw, num(loss)) for q, tat, resp, sw, loss in sweep]
    return table(["Квант q", "Ср. време за обработка", "Ср. време за отговор", "Превключвания",
                  "Загуба за превключване, %"], rows)


def quantum_chart(sweep):
    w, h, ml, mr, mt, mb = 640, 300, 58, 110, 14, 46
    xs = [math.log2(q) for q, *_ in sweep]
    lo, hi = math.log10(40), math.log10(2500)
    px = lambda v: ml + (v - xs[0]) / (xs[-1] - xs[0]) * (w - ml - mr)
    py = lambda v: mt + (hi - math.log10(v)) / (hi - lo) * (h - mt - mb)
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg" '
           'font-family="Times New Roman, serif" font-size="12">']
    for v in (50, 100, 200, 500, 1000, 2000):
        y = py(v)
        out.append(f'<line x1="{ml}" x2="{w - mr}" y1="{y:.1f}" y2="{y:.1f}" stroke="#bbb" stroke-width="0.6"/>')
        out.append(f'<text x="{ml - 6}" y="{y + 4:.1f}" text-anchor="end">{v}</text>')
    for (q, *_), x in zip(sweep, xs):
        out.append(f'<text x="{px(x):.1f}" y="{h - mb + 16}" text-anchor="middle">{q}</text>')
    out.append(f'<line x1="{ml}" x2="{w - mr}" y1="{h - mb}" y2="{h - mb}" stroke="#000" stroke-width="0.8"/>')
    out.append(f'<text x="{(ml + w - mr) / 2}" y="{h - 8}" text-anchor="middle">квант q (логаритмична скала)</text>')
    out.append(f'<text transform="translate(14 {(mt + h - mb) / 2}) rotate(-90)" text-anchor="middle">'
               'време, единици (логаритмична скала)</text>')
    series = [("ср. време за обработка", 1, "", "circle", -6), ("ср. време за отговор", 2, ' stroke-dasharray="6 4"', "square", 14)]
    for name, idx, dash, marker, shift in series:
        pts = [(px(x), py(row[idx])) for x, row in zip(xs, sweep)]
        out.append('<polyline fill="none" stroke="#000" stroke-width="2"' + dash + ' points="'
                   + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')
        for x, y in pts:
            if marker == "circle":
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#fff" stroke="#000" stroke-width="1.5"/>')
            else:
                out.append(f'<rect x="{x - 4:.1f}" y="{y - 4:.1f}" width="8" height="8" fill="#000"/>')
        x, y = pts[-1]
        out.append(f'<text x="{x + 9:.1f}" y="{y + shift:.1f}">{name.replace("ср. време за ", "")}</text>')
    lx, ly = ml + 260, mt + 8
    for i, (name, _, dash, marker, _) in enumerate(series):
        y = ly + i * 18
        out.append(f'<line x1="{lx}" x2="{lx + 34}" y1="{y}" y2="{y}" stroke="#000" stroke-width="2"{dash}/>')
        if marker == "circle":
            out.append(f'<circle cx="{lx + 17}" cy="{y}" r="4" fill="#fff" stroke="#000" stroke-width="1.5"/>')
        else:
            out.append(f'<rect x="{lx + 13}" y="{y - 4}" width="8" height="8" fill="#000"/>')
        out.append(f'<text x="{lx + 42}" y="{y + 4}">{name}</text>')
    out.append("</svg>")
    return "".join(out)


def blocks():
    runs = example_runs()
    load = sim.workload()
    sweep = sim.quantum_sweep(load)
    b = {
        "convoy1": gantt_svg(sim.simulate(sim.CONVOY_LONG_FIRST, "fcfs")),
        "convoy2": gantt_svg(sim.simulate(sim.CONVOY_SHORT_FIRST, "fcfs")),
        "example": example_input(),
        "summary": summary_example(runs),
        "workload": summary_workload(load),
        "quantum-table": quantum_table(sweep),
        "quantum-chart": quantum_chart(sweep),
        "code": "<pre>" + html.escape((SRC / "sim.py").read_text(encoding="utf-8")) + "</pre>",
    }
    for alg, res in runs.items():
        b[f"gantt {alg}"] = gantt_svg(res)
        b[f"table {alg}"] = process_table(res)
    return b


def render(html_path, pdf_path):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                   check=True, capture_output=True)


def page_texts(pdf_path):
    text = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"],
                          check=True, capture_output=True, text=True).stdout
    return [" ".join(p.split()).upper() for p in text.split("\f")]


def main():
    source = (SRC / "referat.html").read_text(encoding="utf-8")
    generated = blocks()

    def fill(m):
        if m[1] not in generated:
            sys.exit(f"unknown marker: {m[1]}")
        return generated[m[1]]

    source = re.sub(r"<!--@([a-z0-9 -]+)-->", fill, source)
    headings = {hid: " ".join(html.unescape(re.sub(r"<[^>]+>", "", t)).split()).upper()
                for hid, t in re.findall(r'<h[12] id="([^"]+)">(.*?)</h[12]>', source)}
    filled = SRC / ".referat.filled.html"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "pass1.pdf"
            filled.write_text(source, encoding="utf-8")
            render(filled, first)
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
            filled.write_text(re.sub(r'<span class="pg" data-for="([^"]+)"></span>',
                                     lambda m: f'<span class="pg" data-for="{m[1]}">{numbers[m[1]]}</span>',
                                     source), encoding="utf-8")
            render(filled, FINAL)
    finally:
        filled.unlink(missing_ok=True)
    print(f"{FINAL.relative_to(OUT.parent.parent.parent)}: {len(page_texts(FINAL)) - 1} pages")


if __name__ == "__main__":
    main()

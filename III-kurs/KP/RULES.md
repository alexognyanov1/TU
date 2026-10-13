# KP: Subject Rules

> Follows the repo-wide [RULES.md](../../RULES.md). Rules here override it for this subject only.

| | |
| --- | --- |
| **Full name (BG)** | Компютърна периферия |
| **Full name (EN)** | Computer Peripherals |
| **Course / semester** | III-kurs, winter semester (2026/27) |
| **Lecturer / assistant** | TODO |

## Required language(s)

- Written work (реферати, презентации, протоколи) is in **Bulgarian**; English technical terms and abbreviations (FIS, NCQ, AHCI, …) may stay as they are.
- Documents are written as self-contained **HTML** (no external resources) and rendered to **PDF** with headless Google Chrome.

## Required techniques / libraries / tools

- Google Chrome (headless `--print-to-pdf`), `pdftotext` (poppler) for the table-of-contents pass, Python 3 standard library.
- Diagrams are inline SVG inside the HTML.
- Commit both the HTML source (`src/`) and the rendered PDFs, so classmates can read them on GitHub without building.

## Not allowed

- No external fonts, CDNs or images loaded from the web: the HTML must render offline.

## Folder layout

- `III-kurs/KP/YYYY.MM.DD/`: one folder per lab day.
- `III-kurs/KP/<TOPIC>/`: реферат / презентация on a topic, e.g. `III-kurs/KP/SATA/` with the PDFs at the top and the sources in `src/`.
- Note: here `KP` is the subject (Компютърна периферия), not "курсов проект".

## How to run

```sh
python3 III-kurs/KP/SATA/src/build.py   # renders SATA_referat.pdf and SATA_prezentatsia.pdf
```

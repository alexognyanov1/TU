# KA: Subject Rules

> Follows the repo-wide [RULES.md](../../RULES.md). Rules here override it for this subject only.

| | |
| --- | --- |
| **Full name (BG)** | Компютърни архитектури |
| **Full name (EN)** | Computer Architectures |
| **Course / semester** | III-kurs, winter semester (2026/27) |
| **Lecturer / assistant** | TODO |

## Required language(s)

- Lab reports are written in **Bulgarian**; English technical terms stay in Latin script.
- Reports are generated as self-contained **HTML** and rendered to **PDF** with headless Google Chrome (Python 3 standard library).

## Required techniques / libraries / tools

- **CPU-OS Simulator** (YASMIN, Windows) for the pipeline experiments: Instruction Pipeline window, its Statistics section (Clocks, CPI, SF, hazards) and the time diagrams.
- Every lab partner gets a separate report with its own styling and wording.

## Not allowed

- Inventing measurements: values that were not captured on a screenshot are marked as missing in the report.

## Folder layout

- `III-kurs/KA/YYYY.MM.DD/`: one folder per lab day, with the handout, the rendered report PDFs and `src/` (`build.py` plus the screenshots in `screens/`).

## How to run

```sh
python3 III-kurs/KA/2026.11.04/src/build.py   # renders both report PDFs into the day folder
```

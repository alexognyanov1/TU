# SS: Subject Rules

> Follows the repo-wide [RULES.md](../../RULES.md). Rules here override it for this subject only.

| | |
| --- | --- |
| **Full name (BG)** | Сигнали и системи |
| **Full name (EN)** | Signals and Systems |
| **Course / semester** | II-kurs |

## Required language(s)

- **Python 3** (course project), MATLAB/Simulink (lab simulations).

## Required techniques / libraries / tools

- `numpy`, `matplotlib`; `python-docx` for generating the report.
- Topics: Fourier spectra of periodic signals, auto/cross-correlation, AM, PAM (АИМ), frequency/phase response of LTI filters.

## Not allowed

- TODO (confirm with the lecturer)

## Folder layout

- `II-kurs/SS/prot/`: lab protocols (`input/` blank templates, `output/` filled-in).
- `II-kurs/SS/KP/`: course project (script + generated report).

## How to run

```sh
pip install numpy matplotlib python-docx
python3 II-kurs/SS/KP/solution.py
```

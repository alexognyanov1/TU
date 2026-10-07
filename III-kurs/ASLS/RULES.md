# ASLS: Subject Rules

> Follows the repo-wide [RULES.md](../../RULES.md). Rules here override it for this subject only.

| | |
| --- | --- |
| **Full name (BG)** | Анализ и синтез на логически схеми (АСЛС) |
| **Full name (EN)** | Analysis and Synthesis of Logic Circuits |
| **Course / semester** | III-kurs, winter semester (2026/27) |
| **Lecturer / assistant** | доц. д-р Георги Запрянов (department of Computer Systems) |

## Required language(s)

- **NI Multisim** schematics for the circuit tasks (Windows only; use the lab PCs or a Windows VM).
- **Python 3** (standard library only) for checking answers by brute force.

## Required techniques / libraries / tools

- Boolean algebra: axioms, theorems and laws from the handout (De Morgan, absorption, reduction, consensus, distributive law). Show each step and name the law used.
- Truth tables, Karnaugh/Veitch maps, minimization.
- Multisim: use the gates named in the handout (7400N, 7402N, 7404N, 7408N, 7432N, 74S86D, 74LS266N, …), interactive digital constants or SPDT switches as inputs, probes as outputs, Word Generator and Logic Analyzer for timing diagrams.

## Not allowed

- Swapping the gates the handout names for other parts, unless the handout allows it (e.g. virtual gates in Fig. 1.13).
- Answers without derivations: each simplification lists the laws used.

## Folder layout

- `III-kurs/ASLS/YYYY.MM.DD/`: one folder per lab day, containing the handout PDF, `README.md` with all answers (derivations, truth tables, Multisim steps), `verify.py` that checks them, and Multisim files (`*.ms14`) or screenshots if any.
- Create a day with `python3 scripts/tu.py new-day III-kurs ASLS --type Lab --lang "Multisim"`.

## How to run

```sh
python3 III-kurs/ASLS/2026.10.07/verify.py    # checks every simplification, prints all truth tables
```

Multisim files: open them in NI Multisim, then Simulate → Run (F5).

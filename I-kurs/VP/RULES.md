# VP: Subject Rules

> Follows the repo-wide [RULES.md](../../RULES.md). Rules here override it for this subject only.

| | |
| --- | --- |
| **Full name (BG)** | Въведение в програмирането (ВПр) |
| **Full name (EN)** | Introduction to Programming |
| **Course / semester** | I-kurs, winter semester (2024) |

## Required language(s)

- **Python 3**.

## Required techniques / libraries / tools

- Input validation with `try`/`except`, lists/tuples/dicts/sets, slicing, comprehensions, string processing, functions, recursion.
- OOP: classes, inheritance, `super()`, polymorphism, composition.
- Stdlib (`random`, `os`, `shutil`, `csv`, `argparse`, `logging`, `datetime`, `math`). Third-party libraries (`requests`, `prettytable`) only when the task needs them.
- Exam tasks: plain Python only, no third-party libraries.

## Not allowed

- API keys or secrets in code. Read them from `.env` via `python-dotenv`.

## Folder layout

- `I-kurs/VP/Lab/YYYY.MM.DD/`, `I-kurs/VP/Seminar/YYYY.MM.DD/`: files `taskN.py` or `main.py`.
- `I-kurs/VP/ExampleTest/TestN/`: sample exams.

## How to run

```sh
python3 I-kurs/VP/Lab/2024.11.05/task8.py
```

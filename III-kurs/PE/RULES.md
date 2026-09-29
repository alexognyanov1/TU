# PE: Subject Rules

> Follows the repo-wide [RULES.md](../../RULES.md). Rules here override it for this subject only.

| | |
| --- | --- |
| **Full name (BG)** | Програмни езици |
| **Full name (EN)** | Programming Languages |
| **Course / semester** | III-kurs, winter semester (2026/27) |
| **Lecturer / assistant** | Данко Вълков (labs) |

## Required language(s)

- **C++17**, compiled with `clang++ -std=c++17 -Wall -Wextra -pedantic` (Apple clang; `g++` works the same). Code must compile with **no warnings**.
- The lab handouts use pre-standard Borland-style C++ (`#include <iostream.h>`, `void main()`). Modern compilers reject this, so write standard C++ instead: `#include <iostream>`, `std::cout` / `std::cin`, `int main()`.

## Required techniques / libraries / tools

- Object-oriented C++: classes with `private` member variables and `public` member functions, constructors (default and parameterised), destructors, getters/setters, objects accessed both directly (`obj.f()`) and through pointers (`p->f()`).
- Validate input ranges in setters and constructors when the task describes allowed values.
- When a task says "array" (масив), use a plain C++ array (`double a[N]` + a count), not `std::vector`.
- Standard library only (`<iostream>`, `<iomanip>`, `<string>`, `<cmath>`, `<limits>`, `<chrono>`, `<thread>`, …). No external libraries.
- One file per task: `task1.cpp`, `task2.cpp`, … Each file is a complete program with its own `main()`.

## Not allowed

- **No comments in the code** unless explicitly asked for. This overrides the repo-wide R7 suggestion to put your name in a comment.
- No `using namespace std;`, no `<iostream.h>` / `<conio.h>` / other non-standard headers, no `void main()`.
- No global variables except `const` values (e.g. array sizes).
- No committed binaries: build output goes to `III-kurs/PE/.build/` (git-ignored).

## Folder layout

- `III-kurs/PE/YYYY.MM.DD/`: one folder per working day, files `task1.cpp`, `task2.cpp`, … plus the lab handout PDF from that day.
- `III-kurs/PE/KP/`: course project (if any).
- Create a day with `python3 scripts/tu.py new-day III-kurs PE --type Lab --lang "C++17"`.

## How to run

Use `III-kurs/PE/run.sh`, from any directory:

```sh
III-kurs/PE/run.sh task1                  # build + run task1 from the latest day folder
III-kurs/PE/run.sh 2026.09.29 task2       # build + run a task from a specific day
III-kurs/PE/run.sh --build 2026.09.29     # compile every task of a day (warnings shown), don't run
III-kurs/PE/run.sh --list                 # list day folders and their tasks
CXX=g++ III-kurs/PE/run.sh task1          # use a different compiler
```

Manually: `clang++ -std=c++17 -Wall -Wextra -pedantic task1.cpp -o task1 && ./task1`

# Repository Ruleset

These rules apply to everyone who adds anything to this repo: me, classmates sending PRs, and any AI assistant. If a subject's own `RULES.md` disagrees with this file, **the subject rules win for that subject**, except for rules R4 and R5 (the README index), which always apply.

## R1. Structure by course

Everything university-related lives under a course folder:

| Folder | Year |
| --- | --- |
| `I-kurs/` | 1st year (2024/25) |
| `II-kurs/` | 2nd year (2025/26) |
| `III-kurs/` | 3rd year (2026/27) |
| `IV-kurs/` | 4th year (create it when it starts) |

Non-university side projects go in `Personal/<ProjectName>/`, never inside a course folder.

## R2. One folder per subject, named by its abbreviation

- Each subject gets its own folder under its course, named with its **upper-case Latin abbreviation**: `III-kurs/PE/`, `II-kurs/BD/`.
- No spaces or Cyrillic in folder names, so paths stay easy to type and link on GitHub.

## R3. One folder per working day

- Code written on a given day goes in a **date folder** named `YYYY.MM.DD` inside the subject: `III-kurs/PE/2026.09.29/`.
- If a subject has both labs and seminars, group them: `<SUBJECT>/Lab/YYYY.MM.DD/` and `<SUBJECT>/Seminar/YYYY.MM.DD/`. Pick one layout per subject and state it in that subject's `RULES.md`.
- Non-dated work gets a descriptive folder: `KP/` (course project, "курсов проект"), `ExampleTest/`, `prot/` (protocols).
- Inside a day folder, name files `task1.<ext>`, `task2.<ext>`, …, or use a name that says what the file does. For multi-file projects (Java, web), keep the IDE project in the day folder.
- `python3 scripts/tu.py new-day III-kurs PE` creates today's folder and adds its README row for you.

## R4. Every subject has its own ruleset

- Every subject folder **must** contain a `RULES.md` that states:
  1. The full subject name (in Bulgarian and English) and the semester.
  2. **The required programming language(s)**, with version where it matters (e.g. C99, Java 21, Python 3.12, MySQL 8).
  3. **The required techniques, libraries, and tools**: what the lecturer expects to see (e.g. "only `stdio.h`/`stdlib.h`, no external libs", "OOP with interfaces", "pure SQL, no ORM").
  4. What is **not allowed** (e.g. no AI-generated code in exam prep, no global variables).
  5. The folder layout for that subject (flat date folders or `Lab/` + `Seminar/`).
  6. How to run or compile the code.
- Start from [`templates/SUBJECT_RULES.md`](templates/SUBJECT_RULES.md). `python3 scripts/tu.py new-subject III-kurs XYZ` does this for you.
- Code in a subject must follow that subject's `RULES.md`. If the lecturer changes the requirements, update the subject's `RULES.md` in the same commit.

## R5. Everything added as code gets a README entry

The point of the [README](README.md) is that classmates can find things on GitHub with Ctrl+F or GitHub search. So:

- **Every** new day folder, project folder, or standalone piece of code **must** have a row in the matching subject table in `README.md`, **in the same commit** that adds the code.
- A row has the form:
  ```
  | 2026.09.29 | Lab | [III-kurs/PE/2026.09.29](III-kurs/PE/2026.09.29) | C | task1 – bubble sort; task2 – pointer arithmetic, dynamic arrays (malloc/free) |
  ```
- The "What's inside" column must be **searchable**: say what each task does in plain English, and name the concepts, algorithms, and keywords a classmate would search for (e.g. "linked list", "JOIN", "inheritance", "recursion", "FFT"). "Lab 3 tasks" is not acceptable.
- Rows go between the subject's `<!-- index:... -->` markers and are sorted by date, oldest first.
- A new subject gets a new section in the README (under its course) and a row in the course's subject table.
- `python3 scripts/tu.py check` fails if any day or project folder is missing from the README or any subject is missing its `RULES.md`. CI runs it on every push and PR.

## R6. Branches and pull requests

- **Nobody pushes to `main` directly.** All work, including README-only changes, goes on a branch and reaches `main` through a pull request.
- Branch names: `<subject>/<YYYY.MM.DD>` for a day's work (e.g. `pe/2026.09.29`), or `chore/<short-description>` for repo changes (e.g. `chore/update-rules`).
- Open the PR against `main`. The **`readme-index`** check (`python3 scripts/tu.py check`) must pass before the PR can be merged. If it fails, fix the branch (usually a missing or TODO README row) and push again.
- Run `python3 scripts/tu.py check` locally before pushing so the PR goes green on the first try.
- Merge with **Squash and merge**, then delete the branch.
- `main` is protected by a GitHub ruleset that enforces this: PRs required, the `readme-index` check must pass, and no force-pushes or deletion.

```sh
git switch -c pe/2026.09.29
python3 scripts/tu.py new-day III-kurs PE
# ...write code, fill in the README row...
python3 scripts/tu.py check
git add -A && git commit -m "PE 2026.09.29: lab 1 – arrays and pointers"
git push -u origin pe/2026.09.29
gh pr create --base main --fill
```

## R7. Hygiene

- Don't commit build output, IDE workspace state, or OS junk (`.DS_Store`, `*.class`, `*.o`, `a.out`, `out/`, `__pycache__/`, `.idea/workspace.xml`, Office lock files `~$*`). `.gitignore` covers these.
- Never commit secrets (`.env`, API keys).
- Commit messages: `<SUBJECT> YYYY.MM.DD: <short description>`, e.g. `PE 2026.09.29: lab 1 – arrays and pointers`.
- Put your name in a comment at the top of a file if it's your solution to an individual assignment.

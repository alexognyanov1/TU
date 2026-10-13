# Instructions for AI assistants

Follow the repo ruleset in @RULES.md. Before writing code for a subject, read that subject's `RULES.md` (e.g. `III-kurs/PE/RULES.md`) and use only the languages and techniques it lists.

Code must be formatted the way the subject's `RULES.md` says. For C++ in PE that means exactly what Vim's `gg=G` produces: run `III-kurs/PE/run.sh --format [DAY]` after writing code. `run.sh --test` fails on unformatted files.

Every change that adds code must also add or update its row in `README.md` (rule R5). Run `python3 scripts/tu.py check` before finishing.

Never commit to `main` directly (rule R6): work on a branch, push it, and open a PR to `main`.

# BPE: Subject Rules

> Follows the repo-wide [RULES.md](../../RULES.md). Rules here override it for this subject only.

| | |
| --- | --- |
| **Full name (BG)** | Базови програмни езици |
| **Full name (EN)** | Basic Programming Languages |
| **Course / semester** | I-kurs, summer semester (2025) |

## Required language(s)

- **C** (C99), compiled with `gcc`.

## Required techniques / libraries / tools

- Standard headers only: `stdio.h`, `stdlib.h`, `string.h`, `math.h`, `ctype.h`, `stdbool.h`.
- `scanf`/`printf`, conditionals/`switch`, loops, functions, pointers, pointer arithmetic.
- Dynamic memory (`malloc`/`realloc`/`free`), 1D/2D arrays, VLAs, C strings via pointers.
- `typedef struct`, nested structs, text and binary file I/O (`fopen`, `fread`/`fwrite`, `fseek`/`ftell`).

## Not allowed

- C++ features or non-standard libraries.
- Leaking memory. Every `malloc` must have a matching `free`.

## Folder layout

- `I-kurs/BPE/Lab/YYYY.MM.DD/`, `I-kurs/BPE/Seminar/YYYY.MM.DD/`: one `taskN.c` per task.

## How to run

```sh
gcc -std=c99 -Wall -Wextra -o task task1.c -lm && ./task
```

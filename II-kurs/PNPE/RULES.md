# PNPE: Subject Rules

> Follows the repo-wide [RULES.md](../../RULES.md). Rules here override it for this subject only.

| | |
| --- | --- |
| **Full name (BG)** | Платформено-независими програмни езици |
| **Full name (EN)** | Platform-Independent Programming Languages |
| **Course / semester** | II-kurs, winter semester (2025) |

## Required language(s)

- **Java** (JDK 17+; switch expressions, pattern-matching `instanceof`, lambdas).

## Required techniques / libraries / tools

- JDK standard library only (`java.util`, `java.io`/`java.nio.file`, `java.net`, `java.util.regex`, `java.util.stream`).
- OOP: encapsulation, inheritance, abstract classes, interfaces, polymorphism, `equals`/`hashCode`.
- Custom checked exceptions, regex validation, design patterns (Factory, Strategy, DI), serialization, sockets + threads, collections, lambdas and Stream API.
- IntelliJ IDEA: each day folder is its own IDE project (`src/`, `.iml`).

## Not allowed

- External libraries / Maven dependencies.

## Folder layout

- `II-kurs/PNPE/YYYY.MM.DD/`: one IntelliJ project per lab, code in `src/` (`src/TaskN/` for multiple tasks).

## How to run

```sh
cd II-kurs/PNPE/2025.10.13 && javac -d out $(find src -name '*.java') && java -cp out Main
```

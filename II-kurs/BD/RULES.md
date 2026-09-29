# BD: Subject Rules

> Follows the repo-wide [RULES.md](../../RULES.md). Rules here override it for this subject only.

| | |
| --- | --- |
| **Full name (BG)** | Бази от данни |
| **Full name (EN)** | Databases |
| **Course / semester** | II-kurs, summer semester (2026) |

## Required language(s)

- **SQL, MySQL dialect** (MySQL 8+/9, InnoDB, `utf8mb4`).

## Required techniques / libraries / tools

- Schema design: `CREATE TABLE`, primary/foreign keys, `UNIQUE`, `ENUM`, `CHECK`, M:N junction tables.
- Queries: `WHERE`, `ORDER BY`, `INNER`/`LEFT JOIN`, self-join, subqueries, aggregates with `GROUP BY` / `HAVING`.
- Views, transactions (`START TRANSACTION` / `COMMIT` / `ROLLBACK`).
- Stored procedures (`DELIMITER`, `IN`/`OUT` params, `DECLARE ... HANDLER`), cursors, triggers (`SIGNAL SQLSTATE '45000'`).
- Recurring lab schema: `school_sport_clubs`.
- Local DB: MySQL via Docker Compose (see `2026.02.25/`).

## Not allowed

- ORMs or application code. Pure SQL scripts only.

## Folder layout

- `II-kurs/BD/YYYY.MM.DD/`: one folder per lab; files `taskN.sql` or numbered `01_*.sql` scripts.
- `II-kurs/BD/KP*/`: course projects, numbered scripts `01_create_tables.sql` … plus the report.

## How to run

```sh
docker compose -f II-kurs/BD/2026.02.25/docker-compose.yml up -d
mysql -h 127.0.0.1 -u root -p < file.sql
```

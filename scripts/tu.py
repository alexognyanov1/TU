#!/usr/bin/env python3
"""Helpers for keeping the repo layout and README index in sync (see RULES.md).

  python3 scripts/tu.py new-day III-kurs PE [--type Lab|Seminar] [--date YYYY.MM.DD] [--lang C]
  python3 scripts/tu.py new-subject III-kurs XYZ
  python3 scripts/tu.py check
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
TEMPLATE = ROOT / "templates" / "SUBJECT_RULES.md"
COURSE_RE = re.compile(r"^[IV]+-kurs$")
DATE_RE = re.compile(r"^\d{4}\.\d{2}\.\d{2}$")
# Sub-folders of a subject that only group work folders, e.g. BPE/Lab/2025.02.19
GROUPS = {"Lab", "Seminar", "ExampleTest"}
SUBJECT_META = {"RULES.md", "README.md", "run.sh", "test.py"}
IGNORED = {".DS_Store", ".idea", ".vscode", "__pycache__"}


def children(path):
    return sorted(p for p in path.iterdir() if p.name not in IGNORED and not p.name.startswith("."))


def rel(path):
    return path.relative_to(ROOT).as_posix()


def courses():
    return [p for p in children(ROOT) if p.is_dir() and COURSE_RE.match(p.name)]


def subjects():
    return [s for c in courses() for s in children(c) if s.is_dir()]


def work_items():
    """Every folder/file that must have its own README row."""
    for subject in subjects():
        for item in children(subject):
            if item.name in SUBJECT_META:
                continue
            if item.is_dir() and item.name in GROUPS:
                yield from children(item)
            else:
                yield item
    personal = ROOT / "Personal"
    if personal.is_dir():
        yield from (p for p in children(personal) if p.is_dir())


def block_bounds(lines, tag):
    start, end = f"<!-- {tag} -->", f"<!-- /{tag} -->"
    try:
        return lines.index(start), lines.index(end)
    except ValueError:
        sys.exit(f"README.md has no '{start}' ... '{end}' block")


def insert_row(lines, tag, row):
    start, end = block_bounds(lines, tag)
    pos = end
    while pos > start + 1 and not lines[pos - 1].strip():
        pos -= 1
    lines.insert(pos, row)


def cmd_new_day(args):
    subject_dir = ROOT / args.course / args.subject
    if not (subject_dir / "RULES.md").exists():
        sys.exit(f"{rel(subject_dir)} has no RULES.md; run: python3 scripts/tu.py new-subject {args.course} {args.subject}")
    date = args.date or datetime.date.today().strftime("%Y.%m.%d")
    if not DATE_RE.match(date):
        sys.exit("--date must be YYYY.MM.DD")
    day = subject_dir / args.group / date if args.group else subject_dir / date
    day.mkdir(parents=True, exist_ok=True)
    print(f"folder: {rel(day)}")

    lines = README.read_text(encoding="utf-8").split("\n")
    link = f"[{rel(day)}]({rel(day)})"
    if any(link in line for line in lines):
        print("README row already exists")
        return
    row = f"| {date} | {args.type} | {link} | {args.lang} | TODO: describe each task + keywords |"
    insert_row(lines, f"index:{args.course}/{args.subject}", row)
    README.write_text("\n".join(lines), encoding="utf-8")
    print("README row added; replace the TODO before committing (rule R5)")


def cmd_new_subject(args):
    course_dir = ROOT / args.course
    subject_dir = course_dir / args.subject
    rules = subject_dir / "RULES.md"
    subject_dir.mkdir(parents=True, exist_ok=True)
    if not rules.exists():
        text = TEMPLATE.read_text(encoding="utf-8")
        rules.write_text(text.replace("{{COURSE}}", args.course).replace("{{SUBJECT}}", args.subject), encoding="utf-8")
        print(f"created {rel(rules)}; fill in the TODOs")

    lines = README.read_text(encoding="utf-8").split("\n")
    tag = f"index:{args.course}/{args.subject}"
    if f"<!-- {tag} -->" in lines:
        print("README section already exists")
        return
    insert_row(lines, f"subjects:{args.course}",
               f"| [{args.subject}]({args.course}/{args.subject}) | TODO | TODO | [rules]({args.course}/{args.subject}/RULES.md) |")
    _, course_end = block_bounds(lines, f"course:{args.course}")
    section = [
        f"### {args.subject}: TODO full name",
        "",
        f"Rules: [{args.course}/{args.subject}/RULES.md]({args.course}/{args.subject}/RULES.md)",
        "",
        f"<!-- {tag} -->",
        "| Date | Type | Folder | Language | What's inside |",
        "| --- | --- | --- | --- | --- |",
        "",
        f"<!-- /{tag} -->",
        "",
    ]
    lines[course_end:course_end] = section
    README.write_text("\n".join(lines), encoding="utf-8")
    print("README section added")


def cmd_check(_args):
    readme = README.read_text(encoding="utf-8")
    errors = []
    for subject in subjects():
        if not (subject / "RULES.md").exists():
            errors.append(f"missing subject ruleset: {rel(subject)}/RULES.md (R4)")
        if f"<!-- index:{rel(subject)} -->" not in readme:
            errors.append(f"missing README section for {rel(subject)} (R5)")
    for item in work_items():
        if f"]({rel(item)})" not in readme:
            errors.append(f"not listed in README: {rel(item)} (R5)")
    for target in re.findall(r"\]\(([^)#:]+)\)", readme):
        if not (ROOT / target).exists():
            errors.append(f"README links to missing path: {target}")
    for n, line in enumerate(readme.split("\n"), 1):
        if line.startswith("|") and "TODO: describe" in line:
            errors.append(f"README.md:{n} still has a TODO description (R5)")
    for e in errors:
        print(e)
    if errors:
        sys.exit(1)
    print("ok")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new-day", help="create today's folder for a subject and its README row")
    p.add_argument("course")
    p.add_argument("subject")
    p.add_argument("--date", help="YYYY.MM.DD (default: today)")
    p.add_argument("--type", default="Lab", help="Lab / Seminar / Homework … (README column)")
    p.add_argument("--group", choices=sorted(GROUPS - {"ExampleTest"}),
                   help="put the folder under <SUBJECT>/Lab or <SUBJECT>/Seminar")
    p.add_argument("--lang", default="TODO", help="language column in README")
    p.set_defaults(func=cmd_new_day)

    p = sub.add_parser("new-subject", help="create a subject folder, its RULES.md and README section")
    p.add_argument("course")
    p.add_argument("subject")
    p.set_defaults(func=cmd_new_subject)

    sub.add_parser("check", help="verify RULES.md files and README index").set_defaults(func=cmd_check)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

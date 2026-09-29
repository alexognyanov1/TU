#!/usr/bin/env python3
"""Build every task of a PE day folder and run it against its test cases.

Test cases live next to the tasks:

    III-kurs/PE/<DAY>/tests/<task>/<case>.in       stdin fed to the program
    III-kurs/PE/<DAY>/tests/<task>/<case>.expect   optional: lines that must appear
                                                    in the output, in this order

Cases whose name starts with `pdf-` use inputs taken from the lab handout.

Usage:
    III-kurs/PE/test.py                 test the latest day
    III-kurs/PE/test.py 2026.09.29      test a specific day
    III-kurs/PE/test.py 2026.09.29 task2   test one task

Exit code is non-zero if any build or expectation fails. The full report is also
written to III-kurs/PE/.build/<DAY>/test-report.txt.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

PE_DIR = Path(__file__).resolve().parent
BUILD_DIR = PE_DIR / ".build"
CXX = os.environ.get("CXX", "clang++")
CXXFLAGS = ["-std=c++17", "-Wall", "-Wextra", "-pedantic", "-g"]
TIMEOUT = 10
DAY_RE = re.compile(r"^\d{4}\.\d{2}\.\d{2}$")

report = []


def out(line=""):
    print(line)
    report.append(line)


def visible(text):
    return re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", lambda m: {"\b": "\\b", "\r": "\\r"}.get(m.group(), f"\\x{ord(m.group()):02x}"), text)


def block(title, text):
    out(f"    {title}:")
    lines = visible(text).rstrip("\n").split("\n") if text.strip() else ["(empty)"]
    for line in lines:
        out(f"      | {line}")


def build(src, day):
    binary = BUILD_DIR / day / src.stem
    binary.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([CXX, *CXXFLAGS, str(src), "-o", str(binary)], capture_output=True, text=True)
    return binary, result.returncode, result.stderr


def run_case(binary, case_in):
    stdin = case_in.read_text() if case_in else ""
    try:
        result = subprocess.run([str(binary)], input=stdin, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired as e:
        partial = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return stdin, partial, None, "TIMEOUT"
    return stdin, result.stdout + result.stderr, result.returncode, None


def check_expect(output, expect_file):
    missing, pos = [], 0
    for want in expect_file.read_text().splitlines():
        if not want:
            continue
        found = output.find(want, pos)
        if found < 0:
            missing.append(want)
        else:
            pos = found + len(want)
    return missing


def main():
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    days = sorted(p.name for p in PE_DIR.iterdir() if p.is_dir() and DAY_RE.match(p.name))
    day = args[0] if args else (days[-1] if days else None)
    if not day or day not in days:
        sys.exit(f"No day folder '{day}' in III-kurs/PE (have: {', '.join(days) or 'none'})")
    only = args[1].removesuffix(".cpp") if len(args) > 1 else None

    day_dir = PE_DIR / day
    tasks = sorted(day_dir.glob("*.cpp"))
    if only:
        tasks = [t for t in tasks if t.stem == only]
        if not tasks:
            sys.exit(f"No {only}.cpp in {day}")

    totals = {"PASS": 0, "FAIL": 0, "RAN": 0}
    out(f"PE {day}: {len(tasks)} task(s), compiler {CXX} {' '.join(CXXFLAGS)}")

    for src in tasks:
        out()
        out("=" * 72)
        binary, code, warnings = build(src, day)
        if code != 0 or warnings.strip():
            status = "BUILD FAILED" if code != 0 else "BUILD HAS WARNINGS"
            out(f"{src.name}: {status}")
            block("compiler", warnings)
            totals["FAIL"] += 1
            if code != 0:
                continue
        else:
            out(f"{src.name}: built")

        case_dir = day_dir / "tests" / src.stem
        cases = sorted(case_dir.glob("*.in")) if case_dir.is_dir() else []
        if not cases:
            out("  no test cases, running once with empty input")
            cases = [None]

        for case_in in cases:
            name = case_in.stem if case_in else "(no input)"
            stdin, output, code, problem = run_case(binary, case_in)
            expect_file = case_in.with_suffix(".expect") if case_in else None
            missing = check_expect(visible(output), expect_file) if expect_file and expect_file.exists() else []

            if problem:
                verdict = "FAIL"
                detail = f"{problem} after {TIMEOUT}s"
            elif code != 0:
                verdict = "FAIL"
                detail = f"exit code {code}"
            elif missing:
                verdict = "FAIL"
                detail = "expected output missing"
            elif expect_file and expect_file.exists():
                verdict, detail = "PASS", "exit 0, output as expected"
            else:
                verdict, detail = "RAN", "exit 0, no .expect file"
            totals[verdict] += 1

            out()
            out(f"  [{verdict}] {src.stem} / {name}: {detail}")
            block("input", stdin)
            block("output", output)
            for want in missing:
                out(f"    missing: {want!r}")

    out()
    out("=" * 72)
    out(f"Summary: {totals['PASS']} passed, {totals['FAIL']} failed, {totals['RAN']} ran without expectations")

    report_file = BUILD_DIR / day / "test-report.txt"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text("\n".join(report) + "\n")
    print(f"Report written to {report_file.relative_to(PE_DIR.parent.parent)}")
    return 1 if totals["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())

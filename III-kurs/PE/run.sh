#!/usr/bin/env bash
set -euo pipefail

PE_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$PE_DIR/.build"
CXX="${CXX:-clang++}"
CXXFLAGS=(-std=c++17 -Wall -Wextra -pedantic -g)

usage() {
    cat <<EOF
Usage:
  ./run.sh TASK              build and run TASK from the latest day folder
  ./run.sh DAY TASK          build and run TASK from DAY (YYYY.MM.DD)
  ./run.sh --build [DAY]     compile every task in DAY (default: latest) without running
  ./run.sh --list            list day folders and their tasks
  ./run.sh --test [DAY] [TASK]  build every task and run all its test cases (see test.py)

TASK is a file name with or without .cpp, e.g. task1 or task1.cpp.
Binaries go to III-kurs/PE/.build/ (git-ignored).
EOF
}

latest_day() {
    ls -1d "$PE_DIR"/[0-9][0-9][0-9][0-9].[0-9][0-9].[0-9][0-9] 2>/dev/null | sort | tail -1 | xargs -n1 basename 2>/dev/null
}

day_dir() {
    local day="${1:-$(latest_day)}"
    [[ -n "$day" && -d "$PE_DIR/$day" ]] || { echo "No day folder '$day' in III-kurs/PE" >&2; exit 1; }
    echo "$PE_DIR/$day"
}

build() {
    local src="$1" day out
    day="$(basename "$(dirname "$src")")"
    out="$BUILD_DIR/$day/$(basename "$src" .cpp)"
    mkdir -p "$(dirname "$out")"
    "$CXX" "${CXXFLAGS[@]}" "$src" -o "$out" >&2
    echo "$out"
}

case "${1:-}" in
    ""|-h|--help)
        usage
        ;;
    --test)
        shift
        exec "$PE_DIR/test.py" "$@"
        ;;
    --list)
        for d in "$PE_DIR"/[0-9]*.[0-9]*.[0-9]*/; do
            [[ -d "$d" ]] || continue
            echo "$(basename "$d"): $(cd "$d" && ls *.cpp 2>/dev/null | sed 's/\.cpp$//' | tr '\n' ' ')"
        done
        ;;
    --build)
        dir="$(day_dir "${2:-}")"
        for src in "$dir"/*.cpp; do
            [[ -e "$src" ]] || continue
            echo "building $(basename "$dir")/$(basename "$src")"
            build "$src" >/dev/null
        done
        echo "ok"
        ;;
    *)
        if [[ $# -ge 2 ]]; then dir="$(day_dir "$1")"; task="$2"; else dir="$(day_dir)"; task="$1"; fi
        src="$dir/${task%.cpp}.cpp"
        [[ -f "$src" ]] || { echo "No such task: $src" >&2; exit 1; }
        bin="$(build "$src")"
        exec "$bin"
        ;;
esac

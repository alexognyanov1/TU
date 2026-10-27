#!/usr/bin/env bash
set -euo pipefail

OS_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$OS_DIR/.build"
CXX="${CXX:-g++}"
CXXFLAGS=(-std=c++17 -Wall -Wextra -pthread -g)

usage() {
    cat <<EOF
Usage:
  ./run.sh TASK              build and run TASK from the latest day folder with C++ tasks
  ./run.sh DAY TASK          build and run TASK from DAY (YYYY.MM.DD)
  ./run.sh --build [DAY]     compile every task in DAY (default: latest) without running
  ./run.sh --list            list day folders and their C++ tasks

TASK is a file name with or without .cpp, e.g. task1 or task1.cpp.
Binaries go to III-kurs/OS/.build/ (git-ignored).
EOF
}

latest_day() {
    for d in "$OS_DIR"/[0-9][0-9][0-9][0-9].[0-9][0-9].[0-9][0-9]; do
        compgen -G "$d/*.cpp" >/dev/null && basename "$d"
    done | sort | tail -1
}

day_dir() {
    local day="${1:-$(latest_day)}"
    [[ -n "$day" && -d "$OS_DIR/$day" ]] || { echo "No day folder '$day' in III-kurs/OS" >&2; exit 1; }
    echo "$OS_DIR/$day"
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
    --list)
        for d in "$OS_DIR"/[0-9]*.[0-9]*.[0-9]*/; do
            [[ -d "$d" ]] || continue
            echo "$(basename "$d"): $(cd "$d" && ls *.cpp 2>/dev/null | sed 's/\.cpp$//' | sort -V | tr '\n' ' ')"
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

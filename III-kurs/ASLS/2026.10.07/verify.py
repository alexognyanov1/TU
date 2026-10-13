#!/usr/bin/env python3
"""Lab 1: brute-force check of every answer in solutions.md.

Compares each original B1 function with its simplified form on all input
combinations, and prints the truth tables used for B2. Exits non-zero if
any simplification is wrong.

    python3 III-kurs/ASLS/2026.10.07/verify.py
"""
import sys
from itertools import product


def n(x):
    return 1 - x


def table(names):
    return list(product((0, 1), repeat=len(names)))


B1 = [
    ("f1", "ABC",
     lambda A, B, C: (A & n(B)) | (A & B) | (A & B & C) | (n(A) & B & C),
     lambda A, B, C: A | (B & C)),
    ("f2", "ABCD",
     lambda A, B, C, D: (A & (n(B | C) | (A & C)) & B & D) | (A & D),
     lambda A, B, C, D: A & D),
    ("f3", "ABCD",
     lambda A, B, C, D: (A & B) | (n(A) & C) | (B & C & D),
     lambda A, B, C, D: (A & B) | (n(A) & C)),
    ("f4", "ABC",
     lambda A, B, C: (A & (n(B) | n(C))) | (B & C),
     lambda A, B, C: A | (B & C)),
    ("f5", "ABC",
     lambda A, B, C: (A & n(B)) | (B & n(C)) | (n(B) & C) | (n(A) & B),
     lambda A, B, C: (A & n(B)) | (B & n(C)) | (n(A) & C)),
    ("f5 alt", "ABC",
     lambda A, B, C: (A & n(B)) | (B & n(C)) | (n(B) & C) | (n(A) & B),
     lambda A, B, C: (n(A) & B) | (n(B) & C) | (A & n(C))),
    ("f6", "ABC",
     lambda A, B, C: (A | (n(A) & B)) & n(((B & C) | (A & n(C))) & n(A)),
     lambda A, B, C: A | (B & n(C))),
]


def check_b1():
    ok = True
    print("B1: original vs simplified, all input combinations")
    for name, names, original, simplified in B1:
        rows = table(names)
        bad = [r for r in rows if original(*r) != simplified(*r)]
        ones = [i for i, r in enumerate(rows) if simplified(*r)]
        status = "OK" if not bad else f"MISMATCH at {bad}"
        print(f"  {name:7} {status:4}  ones at sets {ones}")
        ok = ok and not bad
    return ok


def check_b2():
    print("\nB2.1: two-input gates")
    print("  A B | AND NAND OR NOR XOR XNOR")
    for a, b in table("AB"):
        row = (a & b, n(a & b), a | b, n(a | b), a ^ b, n(a ^ b))
        print(f"  {a} {b} |  " + "    ".join(str(v) for v in row))

    print("\nB2.2a: XOR(XOR(X1, X2), X3), odd parity")
    for x in table("123"):
        print(f"  {x[0]}{x[1]}{x[2]} -> {x[0] ^ x[1] ^ x[2]}")

    print("\nB2.2b: XNOR(X1^X2, X3^X4), even parity")
    for x in table("1234"):
        print(f"  {x[0]}{x[1]}{x[2]}{x[3]} -> {n((x[0] ^ x[1]) ^ (x[2] ^ x[3]))}")

    print("\nB2.5: f6 circuit vs minimized A + BC'")
    _, _, original, simplified = B1[-1]
    for a, b, c in table("ABC"):
        print(f"  {a}{b}{c} -> circuit {original(a, b, c)}  minimized {simplified(a, b, c)}")


if __name__ == "__main__":
    passed = check_b1()
    check_b2()
    sys.exit(0 if passed else 1)

# PE Lab 5 (2026.11.24): operator overloading (self-study tasks)

Handout: [`Lab5_PE-GM.pdf`](Lab5_PE-GM.pdf) („Предефиниране на операции“). Only the self-study exercises („Задачи за самостоятелна работа“) are implemented, and the files are numbered like those exercises. `task1` contains the handout's Задача 4 (`CBox`), because self-study 1 builds on it. Задача 1, 2 and 3 (the `coord` class) are worked examples and are not part of the exercises. The handout code is pre-standard C++, so it is written in standard C++17.

| File | Exercise | Main concepts |
| --- | --- | --- |
| [task1.cpp](task1.cpp) | Зад. 1, 1.1, 1.2: `CBox` from handout task 4 with new operators `<`, `==`, `-` and a test program | binary operators as member functions (`operator<`, `operator==`, `operator-`), overloads for box/box and box/constant, free operator functions for constant/box, chained expressions (`bBox - aBox - smallBox`) |
| [task2.cpp](task2.cpp) | Зад. 2: class `RINT`, an `int` that allows only `+` (unary and binary), `-` (unary and binary), `*`, `/` | unary operators as member functions, binary operators as friend functions, converting constructor from `int` and no conversion back, overflow and division-by-zero checks with exceptions |
| [task3.cpp](task3.cpp) | Зад. 3: class `Vec4` of four `float` with `operator[]` and `+`, `-`, `*`, `/` for vectors and `float` | `operator[]` returning a reference (const and non-const version), bounds check with `std::out_of_range`, friend operators for vector/vector, free operators for vector/float and float/vector |

Build and run with `III-kurs/PE/run.sh task1` (or `task2`, `task3`), and test with `III-kurs/PE/run.sh --test 2026.11.24`. There are 24 test cases in [`tests/`](tests) and all of them pass with no compiler warnings (also clean under AddressSanitizer/UBSan).

## task1: `CBox` with `<`, `==` and `-` (self-study 1, 1.1, 1.2)

- **The base (handout task 4):** the class and the first part of `main` are the handout's program. It prints `aBox dimensions are 10 4 3` and `bBox dimensions are 10 4 6`: `+` stacks two boxes, so the result has the larger length, the larger width and the sum of the heights.
- **Fixes to the handout code:** `int CBox::operator>(…)` inside the class body has an extra `CBox::` that standard compilers reject, so it is `int operator>(…)`. `using std::cout;` is replaced by writing `std::cout`. The free `operator>` is defined before `main` instead of being declared first and defined after it. Everything else, including the `int` result type of the comparisons, is kept.
- **`<` and `==` (Зад. 1.1)** are written the same way as the handout's `>`: they compare volumes, and each has three forms: box with box and box with a constant as member functions, constant with box as a free function (a member function cannot have a `double` on the left).
- **`==` compares the two `double` volumes exactly**, the same way `>` compares them. Two boxes with different sides and the same volume are equal (`2 3 4` and `6 2 2`).
- **`-` (Зад. 1.1)** is the opposite of `+`: it takes a box off the stack. The result keeps the length and width of the left box, and its height is the difference of the heights. If the right box is taller, the height is 0 (an empty box with volume 0), so a box never gets a negative size. `aBox - smallBox` gives `10 4 2`, which is equal to `mediumBox`.
- `a + b - b == a` is true only when `b` is not longer or wider than `a`, because `+` keeps the larger length and width.
- **Test program (Зад. 1.2):** `main` first shows the new operators on the handout's boxes, then reads two boxes (three sides from 0.01 to 1000 on one line) and a volume to compare with (0 to 1e9), and prints every comparison, `A + B`, `A - B` and `B - A`. As in the handout, the constructor stores the larger of the first two numbers as the length. A wrong line is asked for again, and the program stops with `Input ended` when the input ends.

## task2: `RINT`, a restricted `int` (self-study 2)

- `RINT` holds one private `int`. The only operators it defines are unary `+` and `-` (member functions, no parameters) and binary `+`, `-`, `*`, `/` (friend functions with two parameters), which shows both ways of overloading from the handout.
- **How the other operations are kept out:** there is a constructor from `int`, so `RINT a = 17`, `a + 3` and `3 - a` work, but there is no conversion from `RINT` back to `int`. With such a conversion the compiler would turn a `RINT` into an `int` whenever an operator is missing, and `a % b`, `a < b`, `a++` or `a += b` would all compile. Without it they are compile errors. The value is read with `get()`; there is no `operator<<` either, because the task allows only the six operations. Copying and assignment are the ones the compiler generates.
- **Overflow:** `int` overflow is undefined behaviour, so every operation calculates in `long long` and throws `std::overflow_error` if the result does not fit in an `int` (this covers `max + 1`, `-min` and `min / -1`). Division by zero throws `std::domain_error`.
- `main` shows every operation on `a = 17`, `b = 5`, a longer expression (`-(a + b) * 2 / (b - 1)` = -11) and the two errors, then works as a small calculator: it reads `a + b`, `a - b`, `a * b`, `a / b`, `+ a` or `- a` (separated by spaces) and calculates with `RINT` objects until `q` or the end of the input. Anything else (text, a missing operand, another operator such as `%`, a number that does not fit in an `int`) repeats the instructions.

## task3: `Vec4` (self-study 3)

- `Vec4` holds a plain array `float v[4]`.
- **`operator[]`** returns `float&`, so `a[2] = 30` writes into the vector; a second `const` version returns `const float&` for `const` vectors. Both check the index and throw `std::out_of_range` for anything outside 0–3 instead of reading past the array.
- **The operators** work element by element. There are three forms of each of `+`, `-`, `*`, `/`: vector with vector (friend functions), vector with `float` and `float` with vector (free functions that turn the number into a vector of four equal values and call the first form). `f - a` and `f / a` are calculated in that order, `(f - a[i])` and `(f / a[i])`, so they differ from `a - f` and `a / f`.
- **Division by zero** throws `std::domain_error` when any divisor element is 0, so the result never contains `inf` or `nan`.
- `main` shows all twelve combinations and `operator[]` on fixed vectors, including the two errors (`a / 0`, `a[4]`). It then reads vector `a`, vector `b` (four numbers from -1000000 to 1000000 on one line) and a number `f`, prints all twelve results, and reads an index whose element of `a` is doubled through `operator[]` (a wrong index shows the out-of-range message). A wrong line is asked for again, and the program stops with `Input ended` when the input ends.

## Tests

| Task | Cases |
| --- | --- |
| task1 | the handout program's output (`pdf-handout-adding-boxes`), the demonstration of `<`, `==`, `-`, two boxes and a constant (normal), equal volumes with different sides, boxes with the same length and width (`A + B - B == A`), boundaries (sides 0.01 and 1000, volume 0), invalid values (0, negative, too few/too many numbers, text, empty line, over the maximum), input ending early |
| task2 | the demonstration (all six operations, mixed with `int`, both errors), normal expressions (binary and unary, negative operands, extra spaces), boundaries (`INT_MAX`, `INT_MIN`, 46340 × 46340), division by zero and overflow (`max + 1`, `min - 1`, 46341 × 46341, `min / -1`, `- min`), invalid values (empty line, single number, text, no spaces, `%`, `==`, fraction, number larger than `int`, three operands), input ending early |
| task3 | the demonstration (all twelve combinations, `operator[]` read and write, `a / 0`, `a[4]`), normal vectors, negative numbers and fractions, division by zero (vector element and `f = 0`), boundaries (±1000000), index out of range (4 and -1), invalid values (too few/too many numbers, text, empty line, out of range, fractional index), input ending before `f` and before the index |

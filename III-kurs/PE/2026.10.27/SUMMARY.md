# PE Lab 3 (2026.10.27): parameterised constructors, copy constructor, static members

Handout: [`lab3_PE-GM_TEST.pdf`](lab3_PE-GM_TEST.pdf). The handout is marked as test material ("ТЕСТОВ материал за автоматизацията"). It explains three ideas (a constructor with default parameters, the copy constructor, static data members) and has three exercises: two for self-study ("Задачи за самостоятелна работа") and one extra ("Допълнителни задачи"). The exercises are `task1`–`task3`, written in standard C++17.

| File | Exercise | Main concepts |
| --- | --- | --- |
| [task1.cpp](task1.cpp) | Self-study 1: `Point` and `distance()` | constructor with default parameters, copy constructor with a message, friend function, objects passed by value |
| [task2.cpp](task2.cpp) | Self-study 2: `Student` with a static counter | `static` data member defined outside the class, `static` member function `getCount()`, constructor/destructor counting, object lifetime in a `{ }` block, dynamic array `new[]` / `delete[]` |
| [task3.cpp](task3.cpp) | Extra 3: `Fraction` with overloaded `add()` | reducing with the GCD (НОД) in the constructor, overloaded member functions `add(Fraction)` / `add(int)`, sign normalisation |

Build and run with `III-kurs/PE/run.sh taskN`, and test with `III-kurs/PE/run.sh --test 2026.10.27`. There are 27 test cases in [`tests/`](tests) and all of them pass with no compiler warnings.

## task1: `Point`

- Private `double x, y`. The single constructor `Point(double x = 0, double y = 0)` replaces three constructors (`Point()`, `Point(x)`, `Point(x, y)`), which is the handout's point about default parameters.
- The copy constructor `Point(const Point& p)` copies the coordinates and prints `Copying point`.
- `show()` prints `(x, y)`; `main` prints the point's name in front of it, so the output is `A(0, 0)` exactly as in the handout.
- `friend double distance(Point a, Point b)` reads the private coordinates of both points. It takes them **by value**, as the exercise says, so each call copies two points. That is why the handout's output has `Copying point` twice. `main` stores the distance in a variable first, so both messages appear before the `Разстоянието AB е …` line, again as in the handout.
- The distance uses `std::hypot(dx, dy)` rather than `sqrt(dx*dx + dy*dy)`, so very large coordinates (e.g. `1e200`) do not overflow to `inf`.
- The prompts and the result are in Bulgarian because the handout gives the exact output. Non-numeric input is rejected with `Въведете две числа:`, and end of input prints `Входът свърши` and exits, so the program never hangs.

## task2: `Student` and `static int count`

- Private `std::string name` and `int facultyNumber`. `static int count;` is declared in the class and defined once outside it: `int Student::count = 0;`.
- Every constructor (default, parameterised **and copy**) does `++count`, and the destructor does `--count`, so `count` is always the number of objects that exist right now. The copy constructor is written out because the compiler-generated one would copy an object without counting it.
- `static int getCount()` is called through the class, `Student::getCount()`, without any object.
- **Why `new Student[n]`:** a fixed array `Student s[10]` would construct 10 objects and `getCount()` would print 10, not N. The array is still a plain C++ array (no `std::vector`), just allocated with the exact size N that was read, and released with `delete[]`. After `delete[]` the program prints `Students after delete[]: 0`, which shows that the destructors ran.
- The extra object `Student extra(...)` lives in its own `{ }` block. Inside the block the count is N + 1; the destructor runs at the closing brace, so after the block it is back to N.
- Validation: N must be a whole number from 1 to 10. The name is read with `getline` (so it can contain a space, e.g. `Ivan Petrov`), trimmed, and must not be empty. The faculty number is read as text and must be exactly 9 digits, not starting with `0` (a leading zero would make the `int` shorter than 9 digits), so `12345678a`, `-12345678` and `1234567890` are all rejected. `set()` checks the same rule again (`100000000`–`999999999`). End of input prints `Input ended`, frees the array and exits.

## task3: `Fraction`

- Private `long long num, den`. The constructor calls `reduce()`, which divides both by `std::gcd` (the НОД), moves the sign into the numerator (`6/-8` → `-3/4`) and turns a zero denominator into 1 so the object is always valid. `main` itself never passes 0: it re-asks with `The denominator cannot be 0.`
- `add()` is **overloaded**: `add(const Fraction&)` adds another fraction and `add(int)` adds a whole number. Both return a new `Fraction`, which is reduced by its constructor. The fraction sum uses the common denominator `den / g * f.den` with `g = gcd(den, f.den)` to keep the numbers small.
- `show()` prints `n/d`, or only `n` when the denominator is 1 (`1/6 + 5/6 = 1`).
- `main` first prints the handout's examples, `1/2 + 1/3 = 5/6` and `5/6 + 2 = 17/6`, then reads fractions `a`, `b` and a whole number `n` and prints `a + b` and `(a + b) + n`.
- Inputs are limited to −1 000 000 … 1 000 000. With that limit no intermediate product can overflow `long long`, even for the largest inputs (checked against Python's `fractions` module in the `max-values` case).

## Tests

| Task | Cases |
| --- | --- |
| task1 | handout points (0, 0) and (3, 4) (`pdf-handout`, checks both `Copying point` lines and `Разстоянието AB е 5`), negative coordinates, the same point twice, fractional coordinates, very large values, non-numeric input, input ending after one coordinate, empty input |
| task2 | handout example with N = 2 (`pdf-n2`), N = 1 (minimum), N = 10 (maximum), N out of range (0, 11, −3), non-numeric N, invalid faculty numbers (8 digits, 10 digits, leading zero, letters, negative, empty), empty/blank names, input ending early, empty input |
| task3 | handout sums 1/2 + 1/3 and 5/6 + 2 (`pdf-handout`), reduction and sign on creation, whole-number result, zero numerators, zero denominator rejected, largest allowed values, out-of-range rejected, non-numeric input, input ending early, empty input |

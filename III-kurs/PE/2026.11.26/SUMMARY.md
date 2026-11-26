# PE Lab 5, make-up (2026.11.26): operator overloading (self-study tasks)

Handout: [`lab5.md`](lab5.md) („5. Предефиниране на оператори“, from [TUTelage-Lab/cpp-materials](https://github.com/TUTelage-Lab/cpp-materials/blob/main/lab5/lab5.md)). This is the handout of the group the lab is made up with; the own group's lab 5 handout is solved in [`2026.11.24`](../2026.11.24). Only the three self-study exercises („Задачи за самостоятелна работа“) are implemented. Примери 1–4 (`Vector2D`, `Fraction`, `Matrix2x2`, `Polynomial`) are worked examples.

| File | Exercise | Main concepts |
| --- | --- | --- |
| [task1.cpp](task1.cpp) | Задача 1: class `Complex` | `+`, `-`, `*`, `/`, unary `-`, `==`, `!=` as member functions, `magnitude()`, stream operators `<<` and `>>` as friend functions, chained expression `(z1 + z2) * (-z1)` |
| [task2.cpp](task2.cpp) | Задача 2: wrapper classes `LoggedPtr<T>`, `ConfigMap`, `CircularBuffer` | `operator->` and `operator*` of a smart pointer, move assignment that transfers ownership, `operator[]` with a string key that adds missing keys, `operator[]` that maps a logical index to a physical one, deep-copy `operator=`, friend `operator<<` |
| [task3.cpp](task3.cpp) | Задача 3: class `DynArray` | `new[]` / `delete[]`, copy constructor and deep-copy `operator=` with a self-assignment check, `operator[]` with `std::out_of_range`, `operator+` as concatenation, `operator==`, friend `operator<<` |

Build and run with `III-kurs/PE/run.sh 2026.11.26 task1` (or `task2`, `task3`), and test with `III-kurs/PE/run.sh --test 2026.11.26`. There are 27 test cases in [`tests/`](tests) and all of them pass with no compiler warnings (also clean under AddressSanitizer/UBSan). The program output is in English, like the other PE labs, so the handout's log line `[LoggedPtr] -> достъп` is `[LoggedPtr] -> access`.

## task1: `Complex`

- `Complex` has two private `double` fields, `real` and `imag`. The four arithmetic operators, unary `-`, `==` and `!=` are member functions, so the left operand is `*this` and each takes one parameter (unary `-` takes none).
- **Multiplication and division** use the usual formulas: `(a+bi)(c+di) = (ac−bd) + (ad+bc)i` and `(a+bi)/(c+di) = ((ac+bd) + (bc−ad)i) / (c²+d²)`. Division by `0+0i` throws `std::domain_error`, and `main` prints `z1 / z2: division by zero`.
- **`==` compares the two `double` parts exactly**, and `!=` is written as `!(*this == other)`.
- **`operator<<`** always prints the sign between the parts and the imaginary part without its own sign: `3.5+2i`, `3.5-2i`, `0+2i`. A negative zero is printed as `0`.
- **`operator>>`** reads one word in the form `a+bi` or `a-bi` (`3.5+2i`, `-1e3-0.25i`). The word is split at the last `+` or `-` that is not part of an exponent, and both parts must be complete numbers. Anything else (`3.5`, `2i`, `3.5+2`, `1+i`, `3.5 + 2i` with spaces, `inf+1i`) sets `failbit` on the stream and leaves the number unchanged, the way `>>` behaves for built-in types. Both operators return the stream, so they can be chained.
- **`main`** follows the four steps of the exercise: it reads `z1` and `z2` with `>>` (each part from -1000000 to 1000000), prints `+`, `-`, `*`, `/` and `-z1` with `<<`, the chained expression `(z1 + z2) * (-z1)`, the two magnitudes, and `==` / `!=`. A wrong line is asked for again, and the program stops with `Input ended` when the input ends.

## task2: `LoggedPtr<T>`, `ConfigMap`, `CircularBuffer`

- **`LoggedPtr<T>`** is a template that owns a raw pointer. `operator->` prints `[LoggedPtr] -> access` and returns the pointer, so `p->deposit(500.0)` logs and then calls `BankAccount::deposit`. `operator*` returns a reference and does not log. `operator->` cannot know which member is called after it, so the log line is the same for every access.
- **Ownership:** `operator=` takes an rvalue (`q = std::move(p)`). It deletes the object `q` owned before, takes the pointer of `p` and sets `p` to `nullptr`. Copying is disabled, so two `LoggedPtr` objects never delete the same object. The destructor calls `delete`; `BankAccount`'s destructor prints a line, which shows when that happens. Using `->` or `*` on an empty `LoggedPtr` throws `std::logic_error` instead of dereferencing `nullptr`. `std::unique_ptr` is not used.
- **`ConfigMap`** keeps two parallel plain arrays, `std::string keys[8]` and `std::string values[8]`, and a count. `operator[]` returns a reference to the value of an existing key; for a missing key it adds the pair with an empty value and returns a reference to it, as `std::map` does, so reading a missing key also adds it. A ninth key throws `std::length_error`. `operator=` copies every pair (checked in the demonstration: changing the copy does not change the original) and returns `*this`, so `other = copy = cfg` works. `operator<<` prints one `key = value` line per pair.
- **`CircularBuffer`** allocates `double` storage with `new[]`. `push` writes at the next position and wraps around, so the oldest element is overwritten when the buffer is full. `operator[]` takes a logical index, where 0 is the newest element and `size - 1` the oldest, converts it to the physical position `(next - 1 - i + capacity) % capacity` and throws `std::out_of_range` for an index outside the stored elements. There is a `const` version too. The copy constructor and `operator=` make a deep copy (new storage, self-assignment check). `operator<<` prints from newest to oldest: `[7, 6, 5, 4, 3]`.
- **`main`** first runs the handout's snippets: the `LoggedPtr<BankAccount>` example, the `cfg["host"]` example, and 7 elements pushed into a buffer of capacity 5, where `buf[0]` and `buf[4]` are compared with the expected 7 and 3. Then it reads commands until `q` or the end of the input: `deposit AMOUNT` (through `->`), `set KEY VALUE` and `get KEY` (through `ConfigMap::operator[]`), `push NUMBER` and `at INDEX` (through `CircularBuffer::operator[]`), and `show`. A wrong command prints the list of commands, and an error (amount not above 0, full map, wrong index) prints `Error: …`.

## task3: `DynArray`

- `DynArray` has the private fields `double* data`, `int size`, `int capacity`. The constructor `DynArray(int capacity)` allocates with `new[]` (a negative capacity throws `std::invalid_argument`), and the destructor frees with `delete[]`.
- **`push`** adds an element at the end. The capacity is fixed, so a push into a full array throws `std::length_error` instead of writing past the storage.
- **`operator[]`** returns `double&`, so `a[1] = 20` writes into the array; a `const` version returns `const double&`. Both throw `std::out_of_range` for an index outside the stored elements (not the capacity).
- **`operator=`** returns immediately on self-assignment, otherwise allocates new storage, copies the elements and only then deletes the old storage. It returns `*this`, so `d = e = b` works. A copy constructor is defined as well, because `operator+` returns a `DynArray` by value and the compiler-generated copy would share the pointer and delete it twice.
- **`operator+`** returns a new array with the elements of the left array followed by those of the right one; its capacity is the sum of the two capacities. `a + b` and `b + a` differ in order.
- **`operator==`** is true when the sizes are equal and every pair of elements is equal; the capacity does not matter.
- **`operator<<`** prints `[1, 2, 3]`, and `[]` for an empty array.
- **`main`** first shows the four steps of the exercise on fixed arrays, together with the deep copy (`c = a`, then changing `c` leaves `a` unchanged), `a = a`, `d = e = b` and the two errors. Then it reads array `a` and array `b` (0 to 8 numbers from -1000000 to 1000000 on one line, an empty line is an empty array), prints them, `a + b` and `a == b`, reads an index and a new value for `a[index]`, and prints the results again. A wrong line is asked for again, and the program stops with `Input ended` when the input ends.

## Tests

| Task | Cases |
| --- | --- |
| task1 (10) | the handout's output formats `3.5+2i`, `3.5-2i` (`pdf-output-format`) and `0+2i` (`pdf-zero-real`), a normal pair, equal numbers, division by `0+0i`, boundaries (±1000000), exponent notation, invalid values (empty line, text, missing part, missing `i`, spaces inside, two signs, out of range, extra word, `inf`, hexadecimal), input ending after `z1`, empty input |
| task2 (7) | the handout's snippets (`pdf-handout-snippets`), normal commands for all three classes, a buffer that wraps (7 pushes, indexes 0, 4, 5 and -1), a full map (ninth key, changing an existing key afterwards), boundaries (amounts 1000000 and 0.01, numbers ±1000000), invalid values (empty line, unknown command, missing or extra arguments, text, amount 0, negative and too large, fractional index, index in an empty buffer), input ending early |
| task3 (10) | the demonstration, normal arrays, equal arrays, two empty arrays, boundaries (8 elements, ±1000000, last index), index out of range (3 and -1), invalid values (9 numbers, text, out of range, `nan`, fractional index, missing or extra value), input ending before array `b` and before the index |

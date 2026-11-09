# PE Lab 4 (2026.11.10): virtual functions and virtual base classes

Handout: [`Lab4_PE-GM.pdf`](Lab4_PE-GM.pdf) („Виртуални функции и виртуални класове“). It covers virtual base classes (виртуални базови класове) in multiple inheritance and virtual functions (виртуални функции), including pure virtual functions (чисто виртуални функции). It has three tasks with complete code („Задача 1–3“) and two self-study exercises („Задачи за самостоятелна работа“): explain what Задача 3 prints and check it by running the program, then add classes for a tiger and an elephant. All of them are done: the three handout programs in `task1`–`task3`, with the errors in the handout code fixed, the explanation of the output below (task3), and the Tiger/Elephant extension in `task4`. The handout code is pre-standard Borland C++, so everything is written in standard C++17.

| File | Exercise | Main concepts |
| --- | --- | --- |
| [task1.cpp](task1.cpp) | Handout task 1: `vehicle` → `motorized` + `road_use` → `car` | multiple inheritance, diamond problem, virtual base class (`virtual public vehicle`), the most-derived class constructs the virtual base, `enum` |
| [task2.cpp](task2.cpp) | Handout task 2: `area` → `rectangle` / `triangle` | pure virtual function (`= 0`), abstract class, `override`, runtime polymorphism through a base-class pointer, virtual destructor |
| [task3.cpp](task3.cpp) | Handout task 3 + self-study 1: the zoo (`ZooAnimal` → `Bear` → `Panda`), what does it print? | virtual functions called from a base-class member function, calling the base version explicitly (`Bear::isA()`), virtual destructor, friend function, linked list through base-class pointers |
| [task4.cpp](task4.cpp) | Self-study 2: add `Tiger` and `Elephant` | new derived classes by analogy, overriding `print()` / `isA()`, objects created with `new` and deleted through `ZooAnimal*` (virtual destructor), input validation |

Build and run with `III-kurs/PE/run.sh taskN`, and test with `III-kurs/PE/run.sh --test 2026.11.10`. There are 20 test cases in [`tests/`](tests) and all of them pass with no compiler warnings (also clean under AddressSanitizer/UBSan).

## Fixes to the handout code (all tasks)

- `#include <iostream.h>` → `<iostream>`, `<string.h>` → `<cstring>`, `void main()` → `int main()`, and `cout` → `std::cout`.
- The typographic quotes `”…”` and `’\n’` in the PDF are replaced with real `"…"` and `'\n'`.
- Members are initialised in the constructor's initializer list, and member functions that don't change the object are `const`.

## task1: virtual base class `vehicle`

- `motorized` and `road_use` both inherit `vehicle` as `virtual public vehicle`, so a `car` (which inherits both) contains **one** `vehicle` part, not two. Without `virtual`, `car` would have two copies of `num_wheels` and `range`, and `showv()` called from `car` would be ambiguous.
- With a virtual base, the **most-derived class** constructs it: `car`'s constructor calls `vehicle(w, r)` itself, and the `vehicle(w, r)` calls in the initializer lists of `motorized` and `road_use` are skipped when they are built as part of a `car`. `vehicle` has no default constructor, so `car` must call it, as the handout does.
- **Fix:** the handout lists `motorized(m, w, r), road_use(p, w, r), vehicle(w, r)`. Virtual bases are always constructed first, so the list is written in the real order `vehicle(w, r), motorized(…), road_use(…)` (otherwise clang warns with `-Wreorder`).
- **Fix:** the handout's first sketch `class car { ... }; : public motorized, public road_use` doesn't compile; the full program in Задача 1 has the correct form, which is used.
- `showAsVehicle(const vehicle&)` takes the `car` as a `vehicle&`. This conversion compiles only because there is one shared `vehicle` base; with two copies it would be ambiguous.
- `main` creates the handout's `car c(power, gas, 5, 4, 500)` and prints it in the handout's format, then reads the user's own car (steering 1–3, motor 1–3, passengers 1–50, wheels 2–30, range 1–10000) and prints it.

## task2: pure virtual `getarea()`

- `area` stores the two dimensions (private) and declares `virtual double getarea() const = 0;`. It has no meaningful area of its own, so it is a pure virtual function and `area` is an **abstract class**: `area a;` doesn't compile, but `area*` and `area&` can point to a `rectangle` or `triangle`.
- `rectangle::getarea()` returns `d1 * d2` and `triangle::getarea()` returns `0.5 * d1 * d2`, both marked `override`. `p->getarea()` with `area* p` picks the version by the type of the object at run time.
- Added: a **virtual destructor** in `area` (a polymorphic base class should have one), and `getdim()` is `const`.
- `main` runs the handout example (`Rectangle has area: 14.85`, `Triangle has area: 10`), then a menu: choose a rectangle or a triangle, enter two sizes (greater than 0, at most 10000) and the area is printed through the base class (`printArea(const area&)`). Values are printed with the default `std::cout` format, as in the handout, so very large areas appear as `1e+08`.

## task3: the zoo and what it prints (self-study 1)

- **Fixes:** `name`, `sciName` and `indName` are allocated with `new char[]`, so they are freed with `delete[]` (the handout's `delete` is undefined behaviour). String literals are `const char*` in C++, so the parameters are `const char*` (the handout's `char *s = "ZooAnimal"` doesn't compile). The global objects and `headPtr` are moved into `main` (no global variables), and `locTable` is a `const` array. Copying is `= delete`d, because a copy would share the `char*` and delete it twice. The handout text (including the spellings `Adress` and `Melaoleuca`) is kept, so the output can be compared with the prediction.
- **The list:** `makelist` starts at `yinYang` and calls `link()` three times. `link()` inserts the new animal right after `yinYang`, so each new one goes in front of the previous ones: the order is **yinYang → rocky → yogi → circus**.
- **Why the output looks like this:** `print(ZooAnimal*)` is a friend of `ZooAnimal` (so it can read the protected `next`) and calls `pz->print()` for each animal. `print()` is virtual, so the most-derived version runs. `Panda::print()` calls `Bear::print()`, which calls `ZooAnimal::print()`, which calls `isA()`. That call to `isA()` is also virtual, so even from inside `ZooAnimal::print()` it runs `Panda::isA()` for a panda, which prints the name, the scientific name (`Bear::isA()`) and the panda's own name. Explicit calls like `Bear::print()` are not virtual and run exactly that version.
- The program prints (the indented lines start with a tab):

```
Virtual Function Example
Animal name: Big Panda
	Sname: 	Ailuropoda Melaoleuca
	Call our friend: 	Yin Yang
	Adress: 	East B1,P area
	Cell No: 	1001

Animal name: Red Panda
	Sname: 	Ailurus fulgena
	Call our friend: 	Rocky
	Adress: 	East B1,P area
	Cell No: 	943

Animal name: Little bear
	Sname: 	ursus cartoonus
	Adress: 	North B1: brown area

Animal name: Circus animal
```

- `circus` is a plain `ZooAnimal`, so only its name is printed. `yogi` is a `Bear`: name, scientific name and address. The two pandas also print the individual name and the cell number. When `main` ends, the objects are destroyed in reverse order; each destructor frees its own string and then the base destructor runs.

## task4: `Tiger` and `Elephant` (self-study 2)

- Both classes derive from `ZooAnimal` the same way `Bear` does, and the enum and address table get two new places: `TIGER` → `South T1: tiger area`, `ELEPHANT` → `West E1: elephant house`.
- Like `Panda`, each has a species name (`s`, default `Tiger` / `Elephant`), a scientific name (default `Panthera tigris` / `Loxodonta africana`), an individual name and a number: `Tiger` has an enclosure number, `Elephant` a weight in kg. Their `isA()` prints the name, scientific name and individual name; their `print()` adds the address and the number. Their destructors free both strings.
- `main` builds the handout list and links a Bengal tiger `Raja` and an elephant `Tembo` into it, then prints the whole zoo through the same friend `print()`; the new classes need no change to it, which is the point of virtual functions.
- A menu then adds tigers (name of 1–30 characters, enclosure 1–999) and elephants (name, weight 100–10000 kg) from the keyboard, shows the zoo, or exits. New animals are created with `new`, linked into the list and kept in a plain array `ZooAnimal* added[20]`. At the end they are deleted through `ZooAnimal*`, so the virtual destructor runs `~Tiger()` / `~Elephant()` and their strings are freed. After 20 new animals the menu reports that the zoo is full.

## Tests

| Task | Cases |
| --- | --- |
| task1 | the handout car and output (`pdf-handout-car`), own car, lowest and highest values, invalid values (0, 4, -1, text, 2.5, two numbers, empty line, 51, 31, 10001), input ending early, empty input |
| task2 | the handout areas 14.85 and 10 (`pdf-handout-areas`), a rectangle and a triangle, boundaries (10000 × 10000, 0.5 × 0.5, 0.001), invalid values (menu 3/-1/text/empty, sizes 0/-2/text/10001/empty/two numbers), input ending early |
| task3 | the handout output (`pdf-handout-zoo`), input given to the program is ignored |
| task4 | the handout zoo plus `Raja` and `Tembo` (`pdf-handout-zoo-with-tiger-and-elephant`), add a tiger and an elephant and show the zoo (name trimmed), boundaries (enclosure 1 and 999, weight 100 and 10000, 30-character name), invalid values (menu 4/-1/text/empty, empty/blank/31-character name, enclosure 0/1000/text, weight 99/10001/2.5), full zoo (21st animal refused), input ending early |

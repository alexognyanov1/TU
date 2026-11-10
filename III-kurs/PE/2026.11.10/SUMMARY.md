# PE Lab 4 (2026.11.10): virtual functions (self-study tasks)

Handout: [`Lab4_PE-GM.pdf`](Lab4_PE-GM.pdf) („Виртуални функции и виртуални класове“). Only the two self-study exercises („Задачи за самостоятелна работа“) are implemented: explain what Задача 3 prints and check it by running the program, then add classes for a tiger and an elephant. `task3` is Задача 3, the base for both exercises, and keeps its number from the handout. `task4` adds the Tiger/Elephant extension. Задача 1 and 2 are worked examples and are not part of the exercises. The handout code is pre-standard Borland C++, so it is written in standard C++17.

| File | Exercise | Main concepts |
| --- | --- | --- |
| [task3.cpp](task3.cpp) | Handout task 3 + self-study 1: the zoo (`ZooAnimal` → `Bear` → `Panda`), what does it print? | virtual functions called from a base-class member function, calling the base version explicitly (`Bear::isA()`), virtual destructor, friend function, linked list through base-class pointers |
| [task4.cpp](task4.cpp) | Self-study 2: add `Tiger` and `Elephant` | new derived classes by analogy, overriding `print()` / `isA()`, objects created with `new` and deleted through `ZooAnimal*` (virtual destructor), input validation |

Build and run with `III-kurs/PE/run.sh task3` or `task4`, and test with `III-kurs/PE/run.sh --test 2026.11.10`. There are 8 test cases in [`tests/`](tests) and all of them pass with no compiler warnings (also clean under AddressSanitizer/UBSan).

## Fixes to the handout code

- `#include <iostream.h>` → `<iostream>`, `<string.h>` → `<cstring>`, `void main()` → `int main()`, and `cout` → `std::cout`.
- Members are initialised in the constructor's initializer list, and member functions that don't change the object are `const`.

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
| task3 | the handout output (`pdf-handout-zoo`), input given to the program is ignored |
| task4 | the handout zoo plus `Raja` and `Tembo` (`pdf-handout-zoo-with-tiger-and-elephant`), add a tiger and an elephant and show the zoo (name trimmed), boundaries (enclosure 1 and 999, weight 100 and 10000, 30-character name), invalid values (menu 4/-1/text/empty, empty/blank/31-character name, enclosure 0/1000/text, weight 99/10001/2.5), full zoo (21st animal refused), input ending early |

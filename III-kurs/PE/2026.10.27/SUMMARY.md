# PE Lab 3 (2026.10.27): references (псевдоними) and inheritance

Handout: [`Lab3_PE-GM.pdf`](Lab3_PE-GM.pdf). It covers references as function parameters and return values (псевдоними) and inheritance with constructors of derived classes. It has three tasks with complete code („Задача 1–3“) and one self-study exercise („Задачи за самостоятелна работа“). As the lecturer asked, all four are implemented: the three handout programs in `task1`–`task3`, with the errors in the handout code fixed, and the self-study **Media Collection Tool** in `task4`. The handout code is pre-standard Borland C++, so everything is written in standard C++17.

| File | Exercise | Main concepts |
| --- | --- | --- |
| [task1.cpp](task1.cpp) | Handout task 1: distance between two points | `const` reference parameters (`const point&`), why passing by value creates copies whose destructors also run, `static` member function, `const` member function |
| [task2.cpp](task2.cpp) | Handout task 2: bounds-checked `array` | reference as a return value (`char& put(int)` used on the left of `=`), dynamic memory with `new[]` / `delete[]`, bounds checking with `std::out_of_range`, deleted copy constructor (rule of three) |
| [task3.cpp](task3.cpp) | Handout task 3: `vehicle` → `car` / `truck` | public inheritance, derived constructor passing arguments to the base constructor in its initializer list, calling a base member function (`showv()`) from the derived class |
| [task4.cpp](task4.cpp) | Self-study 1: Media Collection Tool (`Item` → `Movie`, `Game`, `Music`) | public inheritance, base-class constructor called from the derived constructor's initializer list, `protected` members, `static` member counter, virtual functions and `override`, abstract base class (pure virtual `play()`), virtual destructor, `const` references as parameters and return values, polymorphism through `Item*` / `const Item&` |

Build and run with `III-kurs/PE/run.sh taskN`, and test with `III-kurs/PE/run.sh --test 2026.10.27`. There are 31 test cases in [`tests/`](tests) and all of them pass with no compiler warnings (also clean under AddressSanitizer/UBSan).

## Fixes to the handout code (all three tasks)

- `void main()` → `int main()`, `<math.h>` → `<cmath>`, and `cout` / `endl` → `std::cout` (the handout has no `using namespace std`, so it doesn't compile).
- The typographic quotes `”…”` and `’X’` in the PDF are replaced with real `"…"` and `'X'`.
- Member functions that don't change the object (`print()`, `get()`, `showv()`, `show()`) are `const`.
- Members are initialised in the constructor's initializer list instead of being assigned in its body.

## task1: `point` and a `const` reference parameter

- **Fix:** `dist(const point&, const point&)` doesn't use the object it is called on (the handout calls it as `a.dist(a, b)`), so it is a `static` member function, called as `point::dist(a, b)`. As a member it can still read the private `x` and `y` of both points.
- `main` first runs the handout example. The output matches the handout: `Creating Point(3,4)`, `Creating Point(10,4)`, `Distance between Point(3,4) and Point(10,4) is 7`, and at the end `Destructing Point(10,4)`, `Destructing Point(3,4)`.
- `distByValue(point, point)` shows the problem from section 1 of the handout. Passed by value, the points are **copied**: no `Creating` line is printed for the copies (the copy constructor runs, not ours), but two extra `Destructing` lines appear when the function returns. `const point&` makes no copies.
- Then the user enters two points as `x y` (any real numbers; invalid lines are asked for again) and their distance is printed.

## task2: bounds-checked `array`

- `char& put(int i)` returns a **reference** to `p[i]`, so `a.put(3) = 'X'` stores into the array. `char get(int i) const` returns a copy of the value.
- **Fix:** the handout checks `if(i=size)`. That is an **assignment**, not a comparison: it sets `i` to 10, which is always true, so every call reports a bounds error. The check is now `i < 0 || i >= size`, in one private `check()` used by both functions.
- **Fix:** `if(!p)` after `new` never fires, because `new` throws `std::bad_alloc` instead of returning a null pointer. The check is removed.
- **Fix:** the handout calls `exit(1)` on a bounds error. That ends the program without running destructors, so the array's memory is never freed. `check()` throws `std::out_of_range` instead, and `main` catches it and prints `Bounds error!!! Index 11 is outside 0..9`.
- **Fix:** the class owns memory from `new[]`, so the copy constructor and copy assignment are `= delete`d. A copy would share `p` and `delete[]` it twice.
- **Fix:** the memory from `new char[num]` is not initialised, so `get()` on an unset index read random data. The constructor fills it with `.`, and a size below 1 becomes 1.
- `main` runs the handout example (`X`, `R`, then the bounds error on `put(11)`), then reads a size (1–100) and the commands `put INDEX CHAR`, `get INDEX` and `show` until end of input.

## task3: `vehicle` → `car` / `truck`

- `car(int p, int w, int r) : vehicle(w, r), passengers(p)` and `truck(int l, int w, int r) : vehicle(w, r), loadlimit(l)` pass the wheels and range to the `vehicle` constructor, as the task asks. `num_wheels` and `range` are private in `vehicle`, so only its constructor can set them, and `car` / `truck` print them through `showv()`.
- `main` creates the handout's `car c(5, 4, 500)` and `truck t(30000, 12, 1200)` and prints them in the handout's format. It then reads a car (passengers 1–50, wheels 2–30, range 1–10000) and a truck (load limit 1–100000, wheels 2–30, range 1–10000) from the keyboard and prints them.

## task4: Media Collection Tool

The class hierarchy follows the UML diagram on the last page of the handout.

**`Item`** (base class, one medium):

- `protected` members exactly as in the diagram: `contentType`, `datePurchased`, `itemID`, `mediaFormat`, `numberOfItems`, `price`, `title`. They are `protected` (`#` in the UML) so the derived classes can use them directly.
- `numberOfItems` is underlined in the diagram, so it is a **`static`** member with a `static` getter `getNumberOfItems()`. The constructor increments it and gives the new item `itemID = numberOfItems`; the destructor decrements it, so it always equals the number of existing items.
- The constructor is `protected` and `play()` is pure virtual, so `Item` is abstract (its name is in italics in the UML). Only `Movie`, `Game` and `Music` can be created.
- Getters for every field, `setItemId()` (rejects IDs below 1) and `virtual toString()`, which builds the message the exercise asks for („<> с заглавие <> е била закупена на цена <> на дата <>“): `Movie (DVD) titled "Inception" was purchased for 19.99 EUR on 12.10.2026.`
- The getters return `const std::string&` / `const Date&`: a reference to the member instead of a copy, the "reference as a return value" idea from handout section 2, but `const` so the caller can't change the object.
- The copy constructor and copy assignment are `= delete`d. A copy would not increment `numberOfItems` but its destructor would decrement it, and copying a polymorphic base would slice the object.
- The media format is an `enum class MediaFormat { DVD, CD, Video }` (the handout's "DVD, CD, видео"), and the purchase date is a small `Date` class that validates day/month/year, including leap years.

**Derived classes**: each constructor passes the common arguments to `Item(...)` in its initializer list (handout section 3, `car(int p, int w, int r) : vehicle(w, r)`) and sets its own content type:

| Class | Extra member (from the exercise / UML) | Extra functions |
| --- | --- | --- |
| `Movie` | `rating` (0–10) | `getRating()`, `playOnDVD()`, `playOnVideo()` |
| `Game` | `difficultyLevel` (1–10), `mfg` (equipment/manufacturer the game runs on) | `getDifficultyLevel()`, `getEquipment()`, `playOnCD()`, `playOnVideo()` |
| `Music` | `bandOrArtist` | `getBandOrArtist()`, `playOnCD()` |

- Each class overrides `toString()`: it calls `Item::toString()` and appends its own field (`Rating: 8.8/10.`, `Difficulty: 7/10, equipment: PC.`, `Artist: The Beatles.`).
- The `playOnX()` functions come from the UML. Each one plays the item only if it is on that medium and returns `false` otherwise. `play()` (the virtual function) tries the class's own `playOnX()` functions in turn, and reports when the medium can't be played (e.g. a movie on CD).
- The UML repeats `getTitle`, `getPrice`, … in every subclass. In C++ these are inherited from `Item` unchanged, so they are not written again.

**`Collection`** holds the items in a plain array `Item* items[20]` plus a count (rule: an array is a plain C++ array). It owns the objects (created with `new`, deleted in its destructor through the virtual destructor) and offers `findById()`, `at(int)` (returns `const Item&`), `changeId()` and `totalPrice()`. When an item is added whose ID is already in use (possible after an ID change), `add()` gives it the smallest free ID with `setItemId()`, so IDs stay unique as the exercise requires. `changeId()` refuses an ID that another item already has.

**`main`** first fills the collection with four sample items, prints them all through `const Item&` (`printItem`) and calls `play()` on each one, which shows polymorphism: the same call runs `Movie::play`, `Game::play` or `Music::play`. Then a menu reads commands from the keyboard: add a movie, game or music item, list the collection, play an item by ID, change an ID, or exit. Every value is read line by line and checked (non-empty title, price 0–100000, format 1–3, a real date as `dd.mm.yyyy` between 1900 and 2100, rating 0–10, difficulty 1–10). Invalid values are asked for again, and end of input at any prompt prints `Input ended` and exits cleanly. Prices are printed in EUR with 2 decimals.

## Tests

| Task | Cases |
| --- | --- |
| task1 | the handout points and output (`pdf-handout-points`), copies made by passing by value, own points (0,0)–(3,4) = 5, the same point twice (distance 0, negative and fractional coordinates), invalid input (text, one number, three numbers, empty line), input ending early |
| task2 | the handout example including the bounds error on `put(11)` (`pdf-handout-array`), `put` / `get` / `show`, out of bounds (index = size and -1, for both `put` and `get`), invalid commands, size validation (0, 101, text), the largest size 100 |
| task3 | the handout car and truck (`pdf-handout-vehicles`), own vehicles, boundaries, invalid values (0, too large, text, 2.5), input ending early |
| task4 | the four sample items and the required message format (`pdf-item-message`), add a movie and play it, add a game and a music item and list them (count and total value), items on a medium they can't be played from, boundaries (price 0 and 100000, rating 0 and 10, difficulty 1 and 10, 29.02 of a leap year, 01.01.1900, 31.12.2100), invalid values (empty title, negative/non-numeric/too large price, format 0/4/text, 29.02.2025, 31.04, wrong date format, month 13, year 1899, rating 11/-1/text, difficulty 0/11/2.5, empty equipment), ID change (ID in use, unknown ID, same ID, then a new item gets the freed ID), unknown ID and invalid ID when playing, invalid menu choices, full collection (20 items), empty input, input ending in the middle of adding an item and of an ID change, non-numeric input |

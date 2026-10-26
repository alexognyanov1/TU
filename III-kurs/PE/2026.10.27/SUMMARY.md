# PE Lab 3 (2026.10.27): references (псевдоними) and inheritance

Handout: [`Lab3_PE-GM.pdf`](Lab3_PE-GM.pdf). It covers references as function parameters and return values (псевдоними) and inheritance with constructors of derived classes. Its "Задача 1–3" come with complete code and are worked examples (point distance with `const point&`, a bounds-checked `array` whose `put()` returns `char&`, and `vehicle` → `car` / `truck`). The only exercise is the self-study one ("Задачи за самостоятелна работа"), the **Media Collection Tool**, which is `task1`. The handout code is pre-standard Borland C++, so the task is written in standard C++17.

| File | Exercise | Main concepts |
| --- | --- | --- |
| [task1.cpp](task1.cpp) | Self-study 1: Media Collection Tool (`Item` → `Movie`, `Game`, `Music`) | public inheritance, base-class constructor called from the derived constructor's initializer list, `protected` members, `static` member counter, virtual functions and `override`, abstract base class (pure virtual `play()`), virtual destructor, `const` references as parameters and return values, polymorphism through `Item*` / `const Item&` |

Build and run with `III-kurs/PE/run.sh task1`, and test with `III-kurs/PE/run.sh --test 2026.10.27`. There are 14 test cases in [`tests/`](tests) and all of them pass with no compiler warnings (also clean under AddressSanitizer/UBSan).

## task1: Media Collection Tool

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
| task1 | the four sample items and the required message format (`pdf-item-message`), add a movie and play it, add a game and a music item and list them (count and total value), items on a medium they can't be played from, boundaries (price 0 and 100000, rating 0 and 10, difficulty 1 and 10, 29.02 of a leap year, 01.01.1900, 31.12.2100), invalid values (empty title, negative/non-numeric/too large price, format 0/4/text, 29.02.2025, 31.04, wrong date format, month 13, year 1899, rating 11/-1/text, difficulty 0/11/2.5, empty equipment), ID change (ID in use, unknown ID, same ID, then a new item gets the freed ID), unknown ID and invalid ID when playing, invalid menu choices, full collection (20 items), empty input, input ending in the middle of adding an item and of an ID change, non-numeric input |

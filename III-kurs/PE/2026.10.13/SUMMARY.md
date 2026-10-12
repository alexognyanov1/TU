# PE Lab 2 (2026.10.13): function overloading and friend functions

Handout: [`lab2_PE-GM.pdf`](lab2_PE-GM.pdf). It has two worked examples and four exercises: two for self-study ("Задачи за самостоятелна работа") and two extra ("Допълнителни задачи"). The exercises are `task1`–`task4`. The handout code is pre-standard Borland C++ (`iostream.h`, `void main()`), so every task is written in standard C++17 instead.

| File | Exercise | Main concepts |
| --- | --- | --- |
| [task1.cpp](task1.cpp) | Self-study 1: rectangle with two `face()` functions | function overloading on member functions, returning a second result through a pointer, constructor and destructor |
| [task2.cpp](task2.cpp) | Self-study 2: extend handout examples 2 and 3 with a travel-time friend function | free friend of two classes, member function of one class that is a friend of another, forward declaration |
| [task3.cpp](task3.cpp) | Extra 3: `Stack` and overloaded `loadstack()` | overloading free functions, returning objects by value, array-based stack |
| [task4.cpp](task4.cpp) | Extra 4: shared printer, `inuse()` | one friend function shared by two classes |

Build and run with `III-kurs/PE/run.sh taskN`, and test with `III-kurs/PE/run.sh --test 2026.10.13`. There are 29 test cases in [`tests/`](tests) and all of them pass with no compiler warnings.

## task1: `rectangle`

Works like the handout's `triangle` class.

- Private sides `a`, `b`. The constructor reads them from the keyboard in a `do … while` loop until both are positive, just as `triangle` repeats until the three sides are valid.
- `double face() const` returns the area `a * b`.
- `double face(double* p) const` is the **overload**. It also returns the area, and writes the perimeter `2 * (a + b)` through the pointer argument. The compiler picks the overload from the arguments: `r1.face()` or `r2.face(&p)`.
- `show(const char*)` prints the sides. It takes `const char*` because string literals are `const` in standard C++, unlike the handout's `char*`.
- The destructor prints `Destructing object rectangle!`. It runs for `r2` and then `r1` at the end of `main`.
- `main` mirrors the handout: `r1` uses `face()`, `r2` uses `face(&p)`, and one extra call goes through a pointer (`pr->face()`).
- `readDouble()` re-asks on non-numeric input and exits cleanly with `Input ended` at end of input, so the validation loop can never spin forever.

## task2: `car` / `truck` with `travel_time()`

The exercise says to extend **both** handout examples, so the file holds both versions in two namespaces with the same vehicles as the handout (`c1(6, 55)`, `c2(2, 120)`, `t1(10000, 55)`, `t2(20000, 72)`).

| | `namespace standalone` (handout task 2) | `namespace member` (handout task 3) |
| --- | --- | --- |
| Speed comparison | `friend int sp_greater(car, truck)`, declared in both classes | `int car::sp_greater(truck)`, and in `truck`: `friend int car::sp_greater(truck)` |
| **New:** travel time | `friend double travel_time(car, truck, double km, double* truck_hours)` | `double car::travel_time(truck, double km, double* truck_hours)`, and a `friend` of `truck` |
| Called as | `sp_greater(c1, t1)`, `travel_time(c1, t1, km, &h)` | `c1.sp_greater(t1)`, `c1.travel_time(t1, km, &h)` |

- `class truck;` is the forward declaration that lets `car` mention `truck` before it is defined.
- `travel_time` uses **T = S / V**. It reads the private `speed` of both objects, which is why it has to be a friend. It returns the car's time and writes the truck's time through the pointer, the same "second result through a pointer" idea as task1.
- The member version only takes the truck as a parameter, because the car is `this`.
- The distance `S` is read from the keyboard and must be positive. Times are printed with 2 decimals, together with which vehicle arrives first and by how much.
- `getPassengers()` / `getWeight()` exist so the handout's `passengers` and `weight` fields are actually used. They appear in the "Comparing …" lines, and without them clang warns about unused private fields.
- The car's time is stored in a variable before `printTimes()` is called. Passing `travel_time(…, &truckHours)` and `truckHours` as arguments of the same call would be a bug, because C++ doesn't fix the order in which arguments are evaluated.

## task3: `Stack` and `loadstack()`

- `Stack` keeps a plain `char data[26]` plus a `top` index. `push` returns `false` when the stack is full, and `pop(char*)` returns `false` when it is empty, so there is never an overflow or underflow.
- `Stack loadstack()` returns a stack filled with `a`–`z`.
- `Stack loadstack(int upper)` is the **overload**. It fills `A`–`Z` when `upper == 1` and `a`–`z` for any other value, as the exercise says.
- Both return the `Stack` by value. The object is copied out of the function, which is why the class needs no dynamic memory.
- `main` prints `loadstack()`, `loadstack(1)` and `loadstack(0)`, then reads `upper` from the keyboard. Popping prints the letters in reverse (LIFO): `zyx…a`. It also shows a pop through a pointer, a push onto a full stack (rejected) and a pop from an empty stack (rejected).

## task4: shared printer, `inuse()`

- `pr1` and `pr2` are the handout's classes: a private `int printing`, a constructor that sets it to 0, and `set_print(int)`.
- `bool inuse(const pr1&, const pr2&)` is declared as a `friend` in **both** classes, after the forward declaration `class pr2;`. It returns `true` when either object is printing, and `false` otherwise.
- The objects are passed by `const` reference rather than by value as in the handout's `sp_greater`. That avoids copies, and it shows that `inuse()` only reads the state.
- `main` first runs a fixed scenario (free → pr1 prints → free → pr2 prints → both print → free). It then reads pairs of statuses (0/1) for `pr1` and `pr2` until end of input. Invalid statuses are rejected, and the objects are updated through pointers.

## Tests

| Task | Cases |
| --- | --- |
| task1 | handout-style sides 30×40 and 10×10 (`pdf-handout-sides`), normal, square, zero and negative sides rejected, non-numeric input, very small/large values, input ending early, empty input |
| task2 | handout vehicles with S = 110 km (`pdf-handout-vehicles`, checks the handout's "speed is the same" and "Car is faster" results for both versions), S = 360, fractional S, zero/negative/non-numeric S rejected, input ending early, empty input |
| task3 | `upper` = 1, 0, 5, -1, non-numeric, empty input |
| task4 | scripted demo, all four status combinations, back to free, out-of-range statuses rejected, non-numeric input, input ending early |

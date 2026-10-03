# TU: University Coursework

Labs, seminars, sample exams and course projects from the **Technical University of Sofia** (Faculty of Computer Systems and Technologies), organised by year and subject.

## How to find something

- **Ctrl+F on this page.** Every folder has a row below that describes what each task does, with keywords like *linked list*, *JOIN*, *inheritance*, *recursion*, *FFT*.
- **GitHub code search.** Press `/` on the repo page and type e.g. `repo:alexognyanov1/TU malloc` or `repo:alexognyanov1/TU path:II-kurs/BD trigger`.
- **Browse by path.** The layout is always `<course>/<SUBJECT>/<YYYY.MM.DD>/`, one folder per working day.

Each subject folder has a `RULES.md` listing the required language, techniques and how to run the code. Repo-wide rules are in [RULES.md](RULES.md).

**Courses:** [I-kurs](#i-kurs-202425) · [II-kurs](#ii-kurs-202526) · [III-kurs](#iii-kurs-202627) · [Personal projects](#personal-projects)

## Adding code

All changes go through a branch and a pull request to `main`. The PR can only be merged once the `readme-index` check passes (rule R6 in [RULES.md](RULES.md)).

```sh
git switch -c pe/2026.09.29                        # one branch per day/change
python3 scripts/tu.py new-day III-kurs PE          # creates III-kurs/PE/<today>/ and a README row
python3 scripts/tu.py new-subject III-kurs XYZ     # new subject: folder, RULES.md, README section
python3 scripts/tu.py check                        # verifies every folder is indexed (also runs in CI)
```

Then replace the `TODO` in the new README row with what each task does (rule R5), commit, push the branch and open a PR (`gh pr create --base main --fill`).

---

<!-- course:III-kurs -->
## III-kurs (2026/27)

Timetable (winter 2026/27, КСИ): [stream 8 PDF](III-kurs/2026-27_winter_KSI_potok8_schedule.pdf) · [stream 9 PDF](III-kurs/2026-27_winter_KSI_potok9_schedule.pdf) · [group 43 JSON](III-kurs/2026-27_winter_KSI_group43_schedule.json)

<!-- subjects:III-kurs -->
| Subject | Name | Language(s) | Rules |
| --- | --- | --- | --- |
| [PE](III-kurs/PE) | Програмни езици / Programming Languages | C++17 | [rules](III-kurs/PE/RULES.md) |

<!-- /subjects:III-kurs -->

### PE: Programming Languages

Rules: [III-kurs/PE/RULES.md](III-kurs/PE/RULES.md) · Build & run: `III-kurs/PE/run.sh [DAY] taskN` · Test all tasks of a day: `III-kurs/PE/run.sh --test [DAY]` ([test.py](III-kurs/PE/test.py), cases in `<DAY>/tests/`)

<!-- index:III-kurs/PE -->
| Date | Type | Folder | Language | What's inside |
| --- | --- | --- | --- | --- |
| 2026.09.29 | Lab | [III-kurs/PE/2026.09.29](III-kurs/PE/2026.09.29) | C++17 | Lab 1 – classes and objects (handout `lab1_PE-GM.pdf`). task1 – `Time` class: hours/minutes/seconds with range-checked setters, print in 24-hour `hh:mm:ss` and 12-hour AM/PM format (`iomanip`, `setw`, `setfill`); task2 – `Worker` class: private members, two constructors (default zero-init / position read from keyboard with `getline`), getters and setters, salaries in a plain array, average and minimum salary; task3 – `Line` class: constructor draws a line of `*`, destructor erases it with backspaces `\b` (object lifetime, automatic destructor call at end of scope, RAII, `std::flush`, `sleep_for`). Input validation and end-of-input handling; 24 stdin test cases in `tests/`. Build & run: `III-kurs/PE/run.sh taskN`, test: `III-kurs/PE/run.sh --test` |

<!-- /index:III-kurs/PE -->

<!-- /course:III-kurs -->

---

<!-- course:II-kurs -->
## II-kurs (2025/26)

<!-- subjects:II-kurs -->
| Subject | Name | Language(s) | Rules |
| --- | --- | --- | --- |
| [PNPE](II-kurs/PNPE) | Платформено-независими програмни езици / Platform-Independent Programming Languages | Java | [rules](II-kurs/PNPE/RULES.md) |
| [SAA](II-kurs/SAA) | Синтез и анализ на алгоритми / Synthesis and Analysis of Algorithms | MATLAB, Python | [rules](II-kurs/SAA/RULES.md) |
| [SS](II-kurs/SS) | Сигнали и системи / Signals and Systems | Python, MATLAB | [rules](II-kurs/SS/RULES.md) |
| [BD](II-kurs/BD) | Бази от данни / Databases | SQL (MySQL) | [rules](II-kurs/BD/RULES.md) |
| [OMT](II-kurs/OMT) | Основи на мрежовите технологии / Fundamentals of Network Technologies | HTML, CSS, JS | [rules](II-kurs/OMT/RULES.md) |

<!-- /subjects:II-kurs -->

### PNPE: Platform-Independent Programming Languages (Java)

Rules: [II-kurs/PNPE/RULES.md](II-kurs/PNPE/RULES.md). Each folder is an IntelliJ project.

<!-- index:II-kurs/PNPE -->
| Date | Type | Folder | Language | What's inside |
| --- | --- | --- | --- | --- |
| 2025.10.09 | Lab | [II-kurs/PNPE/2025.10.09](II-kurs/PNPE/2025.10.09) | Java | BMI calculator class: Scanner input, BMI classification (underweight/normal/overweight/obese), printf; intro to classes and methods |
| 2025.10.13 | Lab | [II-kurs/PNPE/2025.10.13](II-kurs/PNPE/2025.10.13) | Java | 20 basic tasks with a switch menu: max, even/odd, day of week, weekend check (HashSet), ranges, loops, divisibility, min/max/sum, read until "Stop", time + 15 min, factorial/combinatorics with BigInteger, film budget, areas of shapes |
| 2025.10.16 | Lab | [II-kurs/PNPE/2025.10.16](II-kurs/PNPE/2025.10.16) | Java | OOP basics: Company with BULSTAT validation (IllegalArgumentException), SingleOwnerCompany inheritance/super/toString; Car POJO filter, sort with Comparator lambda, remove duplicates via LinkedHashSet, equals/hashCode |
| 2025.10.23 | Lab | [II-kurs/PNPE/2025.10.23](II-kurs/PNPE/2025.10.23) | Java | Abstract class Shape → Circle/Rectangle (area, perimeter), instanceof; interfaces Switchable/Describable implemented by Lamp and TV (multiple interfaces, polymorphism) |
| 2025.10.27 | Lab | [II-kurs/PNPE/2025.10.27](II-kurs/PNPE/2025.10.27) | Java | Arrays Task1–10: fill/print, average, max, sum, sort strings by length (Comparator.comparingInt), linear search, count positive/negative, common elements, reverse in place (two pointers), remove value |
| 2025.10.29 | Lab | [II-kurs/PNPE/2025.10.29](II-kurs/PNPE/2025.10.29) | Java | Custom checked exceptions: Student / ForeignStudent validation (name capitalization, faculty number length, country), try/catch, multi-catch, throws |
| 2025.11.05 | Lab | [II-kurs/PNPE/2025.11.05](II-kurs/PNPE/2025.11.05) | Java | Chess move validator with regex (Pattern/Matcher): algebraic notation, castling, captures, promotion, check/mate, game result |
| 2025.11.10 | Lab | [II-kurs/PNPE/2025.11.10](II-kurs/PNPE/2025.11.10) | Java | Design patterns: Factory (MessageFactory Email/SMS/Push), dependency injection / Strategy (Logger), abstract PaymentMethod (CreditCard/PayPal); Serializable Book list with ObjectOutputStream/ObjectInputStream |
| 2025.11.13 | Lab | [II-kurs/PNPE/2025.11.13](II-kurs/PNPE/2025.11.13) | Java | Multithreaded TCP client/server (ServerSocket, Socket, Runnable per client, readUTF/writeUTF) with REPORT/APPEND/REPLACE/HISTORY commands, synchronized file I/O, .env config parser |
| 2025.11.20 | Lab | [II-kurs/PNPE/2025.11.20](II-kurs/PNPE/2025.11.20) | Java | Bank queue simulation with collections: HashSet, LinkedList, ArrayDeque as FIFO queue and as stack (undo operations), Comparator reversed, packages model/service/util |
| 2025.11.24 | Lab | [II-kurs/PNPE/2025.11.24](II-kurs/PNPE/2025.11.24) | Java | Lambdas and Stream API: filter/sort numbers, products by category/price, student stats (mapToDouble, OptionalDouble, Collectors.partitioningBy), word transforms (distinct, thenComparing), custom @FunctionalInterface, method references |

<!-- /index:II-kurs/PNPE -->

### SAA: Synthesis and Analysis of Algorithms

Rules: [II-kurs/SAA/RULES.md](II-kurs/SAA/RULES.md)

<!-- index:II-kurs/SAA -->
| Date | Type | Folder | Language | What's inside |
| --- | --- | --- | --- | --- |
| 2025.10.07 | Lab | [II-kurs/SAA/2025.10.07](II-kurs/SAA/2025.10.07) | Python | task1 – value frequency counting with a lookup array (counting sort style histogram) |
| 2025.10.21 | Lab | [II-kurs/SAA/2025.10.21](II-kurs/SAA/2025.10.21) | MATLAB | Sorting algorithms: bubble sort (+ early-exit flag), selection, insertion, shell sort (Knuth gaps), quicksort (Hoare partition), heapsort; task1 – timing comparison with tic/toc on 10 000 random ints |
| — | Course project | [II-kurs/SAA/course-project](II-kurs/SAA/course-project) | PDF | Course paper: data and image compression, LZW algorithm (encoder/decoder, dictionary as trie/hash table, GIF/TIFF/PDF usage, comparison with Deflate) |

<!-- /index:II-kurs/SAA -->

### SS: Signals and Systems

Rules: [II-kurs/SS/RULES.md](II-kurs/SS/RULES.md)

<!-- index:II-kurs/SS -->
| Date | Type | Folder | Language | What's inside |
| --- | --- | --- | --- | --- |
| — | Protocols | [II-kurs/SS/prot](II-kurs/SS/prot) | docx | Lab protocols 1–5: spectrum/harmonics of periodic signals, autocorrelation function (ACF), amplitude modulation (AM, modulation index), pulse-amplitude modulation (PAM / АИМ), frequency and phase response (АЧХ/ФЧХ), low-pass filter |
| — | Course project | [II-kurs/SS/KP](II-kurs/SS/KP) | Python | Correlation analysis of exponential signals: autocorrelation R11/R22, cross-correlation R21, numpy/matplotlib plots, report generated with python-docx (OMML equations) |

<!-- /index:II-kurs/SS -->

### BD: Databases

Rules: [II-kurs/BD/RULES.md](II-kurs/BD/RULES.md)

<!-- index:II-kurs/BD -->
| Date | Type | Folder | Language | What's inside |
| --- | --- | --- | --- | --- |
| 2026.02.25 | Lab | [II-kurs/BD/2026.02.25](II-kurs/BD/2026.02.25) | SQL, Docker | MySQL via docker-compose; school DB schema (students, clubs, trainers, groups), CREATE TABLE, INDEX, ENUM, idempotent FOREIGN KEY (information_schema, PREPARE/EXECUTE), ON DELETE CASCADE/SET NULL |
| 2026.03.11 | Lab | [II-kurs/BD/2026.03.11](II-kurs/BD/2026.03.11) | SQL | school_sport_clubs schema, INSERT/DELETE, ORDER BY, multi-table JOIN, DISTINCT; car_service DB design with M:N junction tables |
| 2026.03.19 | Lab | [II-kurs/BD/2026.03.19](II-kurs/BD/2026.03.19) | SQL | JOIN queries by sport/coach/student/time; hospital DB design (doctors, patients, medications, treatments) with named FK constraints |
| 2026.03.25 | Lab | [II-kurs/BD/2026.03.25](II-kurs/BD/2026.03.25) | SQL | cinemas_db design (halls ENUM, screenings), JOIN + IN, SUM; self-join for student pairs, CREATE VIEW, COUNT DISTINCT + GROUP BY |
| 2026.04.01 | Lab | [II-kurs/BD/2026.04.01](II-kurs/BD/2026.04.01) | SQL | GROUP BY + HAVING, LEFT JOIN (coaches without groups), COUNT DISTINCT; transactions (START TRANSACTION/COMMIT) money transfer with subqueries |
| 2026.04.08 | Lab | [II-kurs/BD/2026.04.08](II-kurs/BD/2026.04.08) | SQL | Stored procedures (DELIMITER, IN params, DECLARE, SELECT INTO, IF); sp_transfer_money with transaction, ROW_COUNT(), COMMIT/ROLLBACK; CALL tests |
| 2026.04.15 | Lab | [II-kurs/BD/2026.04.15](II-kurs/BD/2026.04.15) | SQL | Views (salary this month), procedures with GROUP BY/HAVING and LEFT JOIN IS NULL, BGN↔EUR conversion with OUT param, transfer_money with EXIT HANDLER FOR SQLEXCEPTION + ROLLBACK |
| 2026.04.22 | Lab | [II-kurs/BD/2026.04.22](II-kurs/BD/2026.04.22) | SQL | Triggers: AFTER DELETE audit log, BEFORE INSERT with SIGNAL SQLSTATE '45000' (max 2 groups); CHECK constraints, VIEW with LEFT JOIN count; AI test (SUM + HAVING) |
| — | Course project | [II-kurs/BD/KP](II-kurs/BD/KP) | SQL | Topic 12, messaging system DB (users, messages, friendships, blocks): CREATE TABLE, WHERE, GROUP BY, INNER/OUTER JOIN, nested SELECT, triggers, cursor procedure, ON DUPLICATE KEY UPDATE; report |
| — | Course project | [II-kurs/BD/KP2](II-kurs/BD/KP2) | SQL | Topic 13, Twitter/X clone DB (tweets, follows, likes, retweets, hashtags, DMs): sample data, GROUP BY, INNER/LEFT JOIN, subquery, soft-delete trigger with audit log, cursor procedure |

<!-- /index:II-kurs/BD -->

### OMT: Fundamentals of Network Technologies

Rules: [II-kurs/OMT/RULES.md](II-kurs/OMT/RULES.md)

<!-- index:II-kurs/OMT -->
| Date | Type | Folder | Language | What's inside |
| --- | --- | --- | --- | --- |
| 2026.02.19 | Lab | [II-kurs/OMT/2026.02.19](II-kurs/OMT/2026.02.19) | HTML, CSS, JS | Multi-page site with shared nav: headings, links (target=_blank, #anchors), nested ul/ol lists, images with JS lightbox, tables (colspan/rowspan), forms (input types, radio, checkbox, select, textarea) |
| 2026.03.05 | Lab | [II-kurs/OMT/2026.03.05](II-kurs/OMT/2026.03.05) | HTML | Empty index.html placeholder |

<!-- /index:II-kurs/OMT -->

<!-- /course:II-kurs -->

---

<!-- course:I-kurs -->
## I-kurs (2024/25)

<!-- subjects:I-kurs -->
| Subject | Name | Language(s) | Rules |
| --- | --- | --- | --- |
| [VP](I-kurs/VP) | Въведение в програмирането / Introduction to Programming | Python | [rules](I-kurs/VP/RULES.md) |
| [OIP](I-kurs/OIP) | Основи на инженерното проектиране / Fundamentals of Engineering Design | CAD, Python | [rules](I-kurs/OIP/RULES.md) |
| [BPE](I-kurs/BPE) | Базови програмни езици / Basic Programming Languages | C | [rules](I-kurs/BPE/RULES.md) |

<!-- /subjects:I-kurs -->

### VP: Introduction to Programming (Python)

Rules: [I-kurs/VP/RULES.md](I-kurs/VP/RULES.md)

<!-- index:I-kurs/VP -->
| Date | Type | Folder | Language | What's inside |
| --- | --- | --- | --- | --- |
| 2024.10.10 | Lab | [I-kurs/VP/Lab/2024.10.10](I-kurs/VP/Lab/2024.10.10) | Python | Celsius → Fahrenheit (input, f-string, round) |
| 2024.10.15 | Lab | [I-kurs/VP/Lab/2024.10.15](I-kurs/VP/Lab/2024.10.15) | Python | Read up to 10 numbers: even/odd, average, count > 10, try/except |
| 2024.10.22 | Lab | [I-kurs/VP/Lab/2024.10.22](I-kurs/VP/Lab/2024.10.22) | Python | task1 – number → tuple of digits; task2 – random list, insert neighbour sums; task3 – char frequency dict; task4 – dict with zip; task5 – OrderManager class |
| 2024.10.29 | Lab | [I-kurs/VP/Lab/2024.10.29](I-kurs/VP/Lab/2024.10.29) | Python | task1 – OMDb movie API (requests, PrettyTable); task2 – sort files into folders by extension, CSV log; task3 – `tree` directory printer (argparse, recursion); task4 – file backup tool (shutil, os.walk, logging); task5 – Gemini LLM CLI |
| 2024.11.05 | Lab | [I-kurs/VP/Lab/2024.11.05](I-kurs/VP/Lab/2024.11.05) | Python | task1 – area menu; task2 – palindrome number; task3 – calculator with divide-by-zero exception; task4 – threshold replace; task5 – longest word; task6 – Caesar cipher; task7 – Pascal's triangle; task8 – Sudoku solver (backtracking) |
| 2024.11.12 | Lab | [I-kurs/VP/Lab/2024.11.12](I-kurs/VP/Lab/2024.11.12) | Python | OOP: Person class, Student/Lecturer inheritance with super(); text RPG "Battle of the Realms" (Warrior/Mage/Archer, polymorphism) |
| 2024.11.26 | Lab | [I-kurs/VP/Lab/2024.11.26](I-kurs/VP/Lab/2024.11.26) | Python | task1 – Library/Book classes (borrow/return, search); task2 – Zoo: Animal → Mammal/Bird/Reptile inheritance, enclosures |
| 2024.10.16 | Seminar | [I-kurs/VP/Seminar/2024.10.16](I-kurs/VP/Seminar/2024.10.16) | Python | inch → cm, greeting, f-strings, pet food cost, fruit/vegetable price, USD/TRY → EUR currency exchange |
| 2024.10.30 | Seminar | [I-kurs/VP/Seminar/2024.10.30](I-kurs/VP/Seminar/2024.10.30) | Python | task1 – product of numbers divisible by 3 or 4; task2 – min/max/avg; task3 – area/perimeter menu; task4 – date after n days, leap year, weekday; task5 – sum of primes vs non-primes |
| 2024.11.13 | Seminar | [I-kurs/VP/Seminar/2024.11.13](I-kurs/VP/Seminar/2024.11.13) | Python | task1 – dict comprehension; task2 – remove shortest/longest word; task3 – longest run of repeats; task4 – 2D list (matrix), remove row/column; task5 – set operations; task6 – English-Bulgarian dictionary CRUD |
| 2024.12.11 | Seminar | [I-kurs/VP/Seminar/2024.12.11](I-kurs/VP/Seminar/2024.12.11) | Python | OOP: NumericList (isinstance, average), Shape → Square/Circle polymorphism, TriangleChecker, Food/Recipe calorie counter (composition), Employee → Manager/Developer bonuses |
| — | Sample exam | [I-kurs/VP/ExampleTest/Test1](I-kurs/VP/ExampleTest/Test1) | Python | Sample exam 2024: task1 – random list processing (odd indices, negative evens, min/max, filtering); task2 – Car class (sort by price, filter by brand/colour, newest car) |
| — | Sample exam | [I-kurs/VP/ExampleTest/Test2](I-kurs/VP/ExampleTest/Test2) | Python | Sample exam: task1 – list processing (tens digit, index of min, second list, remove/insert); task2 – Worker class for a construction firm (bonus by experience, search, add/remove) |

<!-- /index:I-kurs/VP -->

### OIP: Fundamentals of Engineering Design

Rules: [I-kurs/OIP/RULES.md](I-kurs/OIP/RULES.md)

<!-- index:I-kurs/OIP -->
| Date | Type | Folder | Language | What's inside |
| --- | --- | --- | --- | --- |
| 2024.11.26 | Lab | [I-kurs/OIP/Lab/2024.11.26](I-kurs/OIP/Lab/2024.11.26) | Python | Wi-Fi access point placement with a genetic algorithm (fitness, selection, crossover, mutation), signal coverage heatmap, fitness plot; task1 procedural, task2 class-based |
| 2024.12.03 | Lab | [I-kurs/OIP/Lab/2024.12.03](I-kurs/OIP/Lab/2024.12.03) | Python | Audio signal synthesis: sine, rectangular, symmetric/asymmetric triangle waves, FFT spectrum, save WAV (scipy); MusicGenerator class plays "Für Elise" |

<!-- /index:I-kurs/OIP -->

### BPE: Basic Programming Languages (C)

Rules: [I-kurs/BPE/RULES.md](I-kurs/BPE/RULES.md)

<!-- index:I-kurs/BPE -->
| Date | Type | Folder | Language | What's inside |
| --- | --- | --- | --- | --- |
| 2025.02.19 | Lab | [I-kurs/BPE/Lab/2025.02.19](I-kurs/BPE/Lab/2025.02.19) | C | task1 – char → ASCII code; task2 – rectangle area; task3 – circle circumference (M_PI); task4 – split number into digits; task5 – cylinder area/volume; task6 – seconds → h:m:s |
| 2025.02.28 | Lab | [I-kurs/BPE/Lab/2025.02.28](I-kurs/BPE/Lab/2025.02.28) | C | even/odd, triangle type, month → season (switch), palindrome, sum of multiples, largest digit, average until 0, Fibonacci, GCD (Euclid), prime test, digit count, decimal → binary, digit sum |
| 2025.03.07 | Lab | [I-kurs/BPE/Lab/2025.03.07](I-kurs/BPE/Lab/2025.03.07) | C | GCD, is_prime, digit count, decimal → binary with malloc/free, digit sum; pointer basics (%p), arithmetic via pointer params, swap without temp |
| 2025.03.14 | Lab | [I-kurs/BPE/Lab/2025.03.14](I-kurs/BPE/Lab/2025.03.14) | C | Pointer swap; malloc array: sum, max, average, element closest to average (fabs) |
| 2025.03.21 | Lab | [I-kurs/BPE/Lab/2025.03.21](I-kurs/BPE/Lab/2025.03.21) | C | Strings via pointers: custom strlen, word count (fgets), letter frequency, custom strcmp, vowel count, to_uppercase (toupper) |
| 2025.03.28 | Lab | [I-kurs/BPE/Lab/2025.03.28](I-kurs/BPE/Lab/2025.03.28) | C | 2D arrays / matrices: diagonals, magic square check, rotate matrix 90° (VLA), snake/zigzag fill, submatrix search |
| 2025.04.04 | Lab | [I-kurs/BPE/Lab/2025.04.04](I-kurs/BPE/Lab/2025.04.04) | C | Dynamic arrays: malloc sum/avg, grow with realloc, remove + shrink, merge and sort two arrays, Pascal's triangle (jagged int**) |
| 2025.04.11 | Lab | [I-kurs/BPE/Lab/2025.04.11](I-kurs/BPE/Lab/2025.04.11) | C | Structs: Point distances (sqrt/pow), Vehicle sort by speed, nested structs Student → Class averages, Book cheapest/most expensive/average price |
| 2025.04.30 | Lab | [I-kurs/BPE/Lab/2025.04.30](I-kurs/BPE/Lab/2025.04.30) | C | File I/O: binary files (fwrite/fread, fseek/ftell), even/odd count, sort to text file, Car records menu (binary + text file) |
| 2025.02.17 | Seminar | [I-kurs/BPE/Seminar/2025.02.17](I-kurs/BPE/Seminar/2025.02.17) | C | Star/char patterns (triangle, hollow rectangle), unit conversions (inches, °C → °F, degrees → radians, currency), trig functions, areas with Point structs, simple word problems |
| 2025.03.17 | Seminar | [I-kurs/BPE/Seminar/2025.03.17](I-kurs/BPE/Seminar/2025.03.17) | C | max/min until 0, time + 15 min, bonus points, point in rectangle (struct), cheapest transport, pool pipes, vineyard, histogram percentages, ASCII butterfly |
| 2025.03.18 | Seminar | [I-kurs/BPE/Seminar/2025.03.18](I-kurs/BPE/Seminar/2025.03.18) | C | 1D arrays: longest equal run, zigzag check, reverse, rotate by k, k-th smallest (sort), longest increasing subsequence, subarray with target sum, insert at index |
| 2025.03.31 | Seminar | [I-kurs/BPE/Seminar/2025.03.31](I-kurs/BPE/Seminar/2025.03.31) | C | Matrix row/column order check, max neighbour sum, swap rows (pointer arithmetic); friends graph as adjacency list (structs, realloc) |
| 2025.04.16 | Seminar | [I-kurs/BPE/Seminar/2025.04.16](I-kurs/BPE/Seminar/2025.04.16) | C | Party supplies command loop (strcmp), Product/Order struct command processor, anagram check (char count array) |

<!-- /index:I-kurs/BPE -->

<!-- /course:I-kurs -->

---

## Personal projects

Side projects that aren't tied to a course.

| Project | Language | What it does |
| --- | --- | --- |
| [Personal/CityParser](Personal/CityParser) | Python | Converts the GeoNames Bulgaria dump into a JSON city gazetteer (names, lat/lng, region), filtered against the EKATTE settlement registry |
| [Personal/CountryAutoCompare](Personal/CountryAutoCompare) | Python | Flask REST API that scrapes Numbeo (requests + BeautifulSoup) for cost of living / purchasing power comparisons between cities |
| [Personal/FSM](Personal/FSM) | C | Lexical scanner using state-machine checks to count C numeric literals (decimal, octal, hex, float, suffixes) in a file |
| [Personal/FitnessManager](Personal/FitnessManager) | C | Gym membership manager: struct dynamic array (malloc/realloc), writes to a text file, lists members below average price |
| [Personal/GalleryManager](Personal/GalleryManager) | C | Picture gallery: struct arrays (calloc), filters and averages, file writing, parsing with strtok |
| [Personal/GarageDoorProject](Personal/GarageDoorProject) | C++ (Arduino), HTML/JS | ESP32 garage door controller over Bluetooth LE (NimBLE GATT, password auth, NVS, H-bridge PWM) with a Web Bluetooth frontend + docs |
| [Personal/HandlebarsRenderer](Personal/HandlebarsRenderer) | Python | Flask + SQLAlchemy app rendering configurable YouTube IFrame embeds for mobile WebViews |
| [Personal/IsPointInPolygon](Personal/IsPointInPolygon) | Python | Interactive matplotlib map of Sofia districts (GeoJSON); ray-casting point-in-polygon to name the clicked district |
| [Personal/LinkedList](Personal/LinkedList) | C | Doubly linked list: append, forward and backward traversal |
| [Personal/MobileBGHumanTrafficSimulator](Personal/MobileBGHumanTrafficSimulator) | Python | Locust load test simulating human visitors with random user agents |
| [Personal/MostValuableCurrency](Personal/MostValuableCurrency) | Python | Exchange-rate graph (adjacency list) + DFS to find the most valuable currency |
| [Personal/PharmacyInventoryManager](Personal/PharmacyInventoryManager) | C | Pharmacy inventory: parse records with getline/strtok into a struct array, expiry date comparison, discounts |
| [Personal/RepeatingString](Personal/RepeatingString) | C | Detect repeating characters with a bitmask / bitset (bitwise operations) |
| [Personal/SafeTriangle](Personal/SafeTriangle) | HTML/CSS/JS | Dropdown menu with "safe triangle" hover intent (point-in-triangle test) for submenus |
| [Personal/TravellingSalespersonMaps](Personal/TravellingSalespersonMaps) | Python | Travelling salesperson for Bulgarian cities: Held-Karp bitmask DP over OpenRouteService drive times, schedule, folium map |
| [Personal/WordAutoSuggest](Personal/WordAutoSuggest) | Python | Trie (prefix tree) built from a dictionary word list for prefix checking / autocomplete |

# 5. Предефиниране на оператори

Предефинирането на оператори позволява класовете да се използват с вградените оператори (`+`, `-`, `[]`,
`<<` и др.) по начин, аналогичен на примитивните типове. Реализира се чрез **операторни функции**.

```cpp
// Като член-функция (left operand = this)
ReturnType operator#(параметри);

// Като приятелска функция (двата операнда се подават явно)
friend ReturnType operator#(const T& lhs, const T& rhs);
```

Правила:

- Бинарен оператор като **член-функция** приема **един** параметър (десният операнд); левият е `*this`.
- Бинарен оператор като **приятелска функция** приема **два** параметъра.
- **Не могат** да се предефинират: `::`, `.`, `.*`, `?:`, `sizeof`.
- Операторите `=`, `[]`, `()`, `->` **трябва** да са член-функции.
- За верижно присвояване (`a = b = c`) връщай `T&` и `*this`.

---

## 1. Аритметични и сравнителни оператори като член-функции

### Пример 1: клас `Vector2D`

Двумерен вектор с предефинирани аритметични и сравнителни оператори.

```cpp
#include <iostream>
#include <cmath>

class Vector2D {
private:
    double x, y;

public:
    Vector2D(double x = 0, double y = 0) : x(x), y(y) {}

    Vector2D operator+(const Vector2D& other) const {
        return {x + other.x, y + other.y};
    }

    Vector2D operator-(const Vector2D& other) const {
        return {x - other.x, y - other.y};
    }

    Vector2D operator*(double scalar) const {
        return {x * scalar, y * scalar};
    }

    bool operator==(const Vector2D& other) const {
        return x == other.x && y == other.y;
    }

    bool operator!=(const Vector2D& other) const {
        return !(*this == other);
    }

    double magnitude() const { return std::sqrt(x * x + y * y); }

    void print() const {
        std::cout << "(" << x << ", " << y << ")";
    }
};

int main() {
    Vector2D v1(3.0, 4.0), v2(1.0, 2.0), v3(0.5, 0.5);

    std::cout << "v1 = "; v1.print(); std::cout << "\n";
    std::cout << "v2 = "; v2.print(); std::cout << "\n";

    Vector2D sum = v1 + v2;
    std::cout << "v1 + v2 = "; sum.print(); std::cout << "\n";

    // Верижна операция: v1 + v2 - v3
    Vector2D chain = v1 + v2 - v3;
    std::cout << "v1 + v2 - v3 = "; chain.print(); std::cout << "\n";

    Vector2D scaled = v1 * 2.0;
    std::cout << "v1 * 2 = "; scaled.print(); std::cout << "\n";

    std::cout << "|v1| = " << v1.magnitude() << "\n";
    std::cout << "v1 == v2: " << (v1 == v2 ? "true" : "false") << "\n";
    std::cout << "v1 != v2: " << (v1 != v2 ? "true" : "false") << "\n";

    return 0;
}
```

**Резултати:**

```text
v1 = (3, 4)
v2 = (1, 2)
v1 + v2 = (4, 6)
v1 + v2 - v3 = (3.5, 5.5)
v1 * 2 = (6, 8)
|v1| = 5
v1 == v2: false
v1 != v2: true
```

---

### Пример 2: клас `Fraction` — дроби с редукция

Операторите са най-полезни, когато абстракцията има математическа семантика. Класът `Fraction` автоматично
съкращава резултатите след всяка операция.

```cpp
#include <iostream>
#include <stdexcept>
#include <numeric>   // std::gcd (C++17)

class Fraction {
private:
    int num, den;

    void reduce() {
        int g = std::gcd(std::abs(num), std::abs(den));
        num /= g;
        den /= g;
        if (den < 0) { num = -num; den = -den; }
    }

public:
    Fraction(int num = 0, int den = 1) : num(num), den(den) {
        if (den == 0) throw std::invalid_argument("Знаменателят не може да е 0");
        reduce();
    }

    Fraction operator+(const Fraction& other) const {
        return {num * other.den + other.num * den, den * other.den};
    }

    Fraction operator-(const Fraction& other) const {
        return {num * other.den - other.num * den, den * other.den};
    }

    Fraction operator*(const Fraction& other) const {
        return {num * other.num, den * other.den};
    }

    Fraction operator/(const Fraction& other) const {
        return {num * other.den, den * other.num};
    }

    bool operator==(const Fraction& other) const {
        return num == other.num && den == other.den;
    }

    void print() const {
        if (den == 1) std::cout << num;
        else          std::cout << num << "/" << den;
    }
};

int main() {
    Fraction a(1, 2), b(1, 3), c(2, 4);   // c се свежда до 1/2

    std::cout << "a = "; a.print(); std::cout << "\n";
    std::cout << "b = "; b.print(); std::cout << "\n";
    std::cout << "c = "; c.print(); std::cout << " (от 2/4)\n";

    Fraction sum = a + b;
    std::cout << "a + b = "; sum.print(); std::cout << "\n";

    Fraction diff = a - b;
    std::cout << "a - b = "; diff.print(); std::cout << "\n";

    Fraction prod = a * b;
    std::cout << "a * b = "; prod.print(); std::cout << "\n";

    Fraction quot = a / b;
    std::cout << "a / b = "; quot.print(); std::cout << "\n";

    // Верижно: (1/2 + 1/3) * 2/1
    Fraction chain = (a + b) * Fraction(2);
    std::cout << "(a + b) * 2 = "; chain.print(); std::cout << "\n";

    std::cout << "a == c: " << (a == c ? "true" : "false") << "\n";

    return 0;
}
```

**Резултати:**

```text
a = 1/2
b = 1/3
c = 1/2 (от 2/4)
a + b = 5/6
a - b = 1/6
a * b = 1/6
a / b = 3/2
(a + b) * 2 = 5/3
a == c: true
```

---

## 2. Оператори за присвояване и съставни оператори

`operator=` **трябва** да е член-функция. Трябва да:

1. Провери за самоприсвояване (`if (this == &other) return *this;`).
2. Почисти собствените ресурси (ако има динамична памет).
3. Копира данните.
4. Върне `*this` като референция, за да позволи верижно `a = b = c`.

Съставните оператори (`+=`, `-=`, ...) също връщат `T&`.

### Пример 3: клас `Matrix2x2`

```cpp
#include <iostream>

class Matrix2x2 {
private:
    double m[2][2];

public:
    Matrix2x2(double a = 0, double b = 0, double c = 0, double d = 0) {
        m[0][0] = a; m[0][1] = b;
        m[1][0] = c; m[1][1] = d;
    }

    Matrix2x2& operator=(const Matrix2x2& other) {
        if (this == &other) return *this;
        for (int i = 0; i < 2; i++)
            for (int j = 0; j < 2; j++)
                m[i][j] = other.m[i][j];
        return *this;
    }

    Matrix2x2& operator+=(const Matrix2x2& other) {
        for (int i = 0; i < 2; i++)
            for (int j = 0; j < 2; j++)
                m[i][j] += other.m[i][j];
        return *this;
    }

    Matrix2x2 operator+(const Matrix2x2& other) const {
        Matrix2x2 result = *this;
        result += other;
        return result;
    }

    Matrix2x2 operator*(const Matrix2x2& other) const {
        return {
            m[0][0]*other.m[0][0] + m[0][1]*other.m[1][0],
            m[0][0]*other.m[0][1] + m[0][1]*other.m[1][1],
            m[1][0]*other.m[0][0] + m[1][1]*other.m[1][0],
            m[1][0]*other.m[0][1] + m[1][1]*other.m[1][1]
        };
    }

    void print() const {
        std::cout << "[ " << m[0][0] << "  " << m[0][1] << " ]\n";
        std::cout << "[ " << m[1][0] << "  " << m[1][1] << " ]\n";
    }
};

int main() {
    Matrix2x2 a(1, 2, 3, 4);
    Matrix2x2 b(5, 6, 7, 8);
    Matrix2x2 c(0, 1, 1, 0);

    // Верижно присвояване
    Matrix2x2 x, y;
    x = y = a;
    std::cout << "x = y = a:\n"; x.print();

    // Съставен оператор
    x += b;
    std::cout << "x += b:\n"; x.print();

    // Събиране чрез +=
    Matrix2x2 sum = a + b;
    std::cout << "a + b:\n"; sum.print();

    // Матрично умножение
    Matrix2x2 prod = a * b;
    std::cout << "a * b:\n"; prod.print();

    return 0;
}
```

**Резултати:**

```text
x = y = a:
[ 1  2 ]
[ 3  4 ]
x += b:
[ 6  8 ]
[ 10  12 ]
a + b:
[ 6  8 ]
[ 10  12 ]
a * b:
[ 19  22 ]
[ 43  50 ]
```

---

## 3. Потокови оператори и оператор за индексиране

`operator<<` и `operator>>` **трябва** да са приятелски функции — левият им операнд е `std::ostream` /
`std::istream`, а не нашият клас.

`operator[]` е член-функция и връща **псевдоним** (`T&`), за да може да се използва от лявата страна
на присвояване.

> Потоковите оператори трябва да връщат `std::ostream&` / `std::istream&`, за да позволят верижно
> `cout << a << b`.

### Пример 4: клас `Polynomial`

Полином от степен `n` с `n+1` коефициента. Коефициентът с индекс `i` е при `x^i`.

```cpp
#include <iostream>
#include <stdexcept>

class Polynomial {
private:
    double* coef;
    int degree;

public:
    Polynomial(int degree = 0) : degree(degree) {
        coef = new double[degree + 1]();
    }

    Polynomial(const Polynomial& other) : degree(other.degree) {
        coef = new double[degree + 1];
        for (int i = 0; i <= degree; i++) coef[i] = other.coef[i];
    }

    ~Polynomial() { delete[] coef; }

    // operator[] — псевдоним за коефициент по индекс
    double& operator[](int i) {
        if (i < 0 || i > degree) throw std::out_of_range("Индекс извън граница");
        return coef[i];
    }

    // operator+ като приятелска функция
    friend Polynomial operator+(const Polynomial& a, const Polynomial& b) {
        int maxDeg = a.degree > b.degree ? a.degree : b.degree;
        Polynomial result(maxDeg);
        for (int i = 0; i <= a.degree; i++) result.coef[i] += a.coef[i];
        for (int i = 0; i <= b.degree; i++) result.coef[i] += b.coef[i];
        return result;
    }

    // operator<< — форматиран изход: "3x^2 + 2x + 1"
    friend std::ostream& operator<<(std::ostream& os, const Polynomial& p) {
        bool first = true;
        for (int i = p.degree; i >= 0; i--) {
            if (p.coef[i] == 0) continue;
            if (!first) os << (p.coef[i] > 0 ? " + " : " - ");
            else if (p.coef[i] < 0) os << "-";
            double abs_c = p.coef[i] < 0 ? -p.coef[i] : p.coef[i];
            if (i == 0)      os << abs_c;
            else if (i == 1) os << abs_c << "x";
            else             os << abs_c << "x^" << i;
            first = false;
        }
        if (first) os << "0";
        return os;
    }
};

int main() {
    Polynomial p1(2), p2(2);

    // Запис чрез operator[]
    p1[2] = 3; p1[1] = 2; p1[0] = 1;   // 3x^2 + 2x + 1
    p2[2] = 1; p2[1] = -1; p2[0] = 4;  // x^2 - x + 4

    std::cout << "p1 = " << p1 << "\n";
    std::cout << "p2 = " << p2 << "\n";

    Polynomial sum = p1 + p2;
    std::cout << "p1 + p2 = " << sum << "\n";

    // Промяна на коефициент чрез operator[]
    p1[0] = 99;
    std::cout << "p1 след p1[0] = 99: " << p1 << "\n";

    return 0;
}
```

**Резултати:**

```text
p1 = 3x^2 + 2x + 1
p2 = x^2 - x + 4
p1 + p2 = 4x^2 + x + 5
p1 след p1[0] = 99: 3x^2 + 2x + 99
```

---

## Задачи за самостоятелна работа

### Задача 1 — Комплексни числа

Дефинирайте клас `Complex` с `private` полета `double real` и `double imag`.

Предефинирайте като **член-функции**:

- `operator+`, `operator-`, `operator*`, `operator/`
- унарен `operator-` (отрицание, без параметри)
- `operator==`, `operator!=`
- `double magnitude() const` — модул: `√(real² + imag²)`

Предефинирайте като **приятелски функции**:

- `operator<<` — извежда във формат `3.5+2i`, `3.5-2i`, `0+2i`
- `operator>>` — въвежда от формат `a+bi` или `a-bi`

Демонстрирайте в `main()`:

1. Въведете два комплексни числа с `>>`.
2. Пресметнете и изведете с `<<` всички аритметични операции.
3. Покажете верижен израз: `(z1 + z2) * (-z1)`.
4. Изведете модулите.

---

### Задача 2 — Wrapper класове: `operator->`, `operator=` и `operator[]`

Операторите `->`, `=` и `[]` се предефинират, когато искаме клас да се **държи като посредник** —
умен указател, прокси, или обвивка около ресурс.

| Оператор     | Типична употреба                                      | Трябва да е член |
|--------------|-------------------------------------------------------|------------------|
| `operator->` | Умен указател — делегира достъп до обвития обект      | Да               |
| `operator=`  | Дълбоко копие / прехвърляне на ресурс                 | Да               |
| `operator[]` | Индексиран достъп с валидация или допълнителна логика | Да               |

```cpp
T* operator->()           // трябва да върне указател (или обект с operator->)
T& operator=(const T& o)  // трябва да върне *this за верижно присвояване
T& operator[](int i)      // обикновено връща псевдоним за четене и запис
```

---

Дефинирайте три класа, демонстриращи трите оператора в реалистичен контекст.

---

**Клас `LoggedPtr<T>` — умен указател с логване**

Шаблонен wrapper около суров указател. Всяко обръщение през `->` отпечатва съобщение кой метод
се достъпва.

```
LoggedPtr<BankAccount> p(new BankAccount("Иван", 1000.0));
p->deposit(500.0);   // лог: "[LoggedPtr] -> достъп"
p->describe();
```

Предефинирайте:

- `T* operator->()` — логва и делегира към вътрешния указател
- `T& operator*()` — дерефериране
- `operator=` — прехвърля собствеността (move семантика: старият `LoggedPtr` става `nullptr`)
- деструктор — освобождава паметта с `delete`

> Забележка: не използвайте `std::unique_ptr` — целта е да имплементирате поведението ръчно.

---

**Клас `ConfigMap` — речник с `operator[]`**

Клас, моделиращ конфигурационен речник (ключ → стойност като `std::string`). Вътрешно използва
два паралелни масива `std::string keys[]` и `std::string values[]` с фиксиран капацитет.

Предефинирайте:

- `std::string& operator[](const std::string& key)` — ако ключът съществува, връща псевдоним към
  стойността; ако не съществува, добавя нова двойка с празна стойност и връща псевдоним към нея (поведение като
  `std::map`)
- `operator=` — дълбоко копие на целия речник
- `operator<<` (приятелска) — извежда всички двойки ключ-стойност

```cpp
ConfigMap cfg;
cfg["host"] = "localhost";
cfg["port"] = "5432";
cfg["db"]   = "mydb";
std::cout << cfg;
```

---

**Клас `CircularBuffer` — пръстеновиден буфер с `operator[]`**

Буфер с фиксиран размер, при препълване презаписва най-стария елемент. Индексирането е **относително
спрямо текущата позиция** — `buf[0]` е най-новият елемент, `buf[n-1]` е най-старият.

Предефинирайте:

- `double& operator[](int i)` — транслира логически индекс към физически, хвърля `std::out_of_range`
  при невалиден индекс
- `operator=` — дълбоко копие
- `operator<<` (приятелска) — извежда елементите от най-новия към най-стария

Демонстрирайте: добавете 7 елемента в буфер с капацитет 5, изведете с `<<`, достъпете `buf[0]`
и `buf[4]` и ги сравнете с очакваните стойности.

---

### Задача 3 — Динамичен масив от числа

Дефинирайте клас `DynArray` с `private` полета `double* data`, `int size`, `int capacity`.

Предефинирайте:

- `operator[]` (член) — връща `double&`, проверява индекса с `std::out_of_range`
- `operator=` (член) — дълбоко копие, защита от самоприсвояване
- `operator+` (член) — конкатенация на два масива, връща нов `DynArray`
- `operator==` (член) — поелементно сравнение
- `operator<<` (приятелска) — извежда `[1, 2, 3]`

Класът трябва да има:

- конструктор `DynArray(int capacity)` — заделя памет с `new`
- деструктор — освобождава с `delete[]`
- метод `void push(double val)` — добавя елемент (проверява капацитета)

Демонстрирайте в `main()`:

1. Създайте два масива, попълнете ги с `push()`.
2. Достъпете и променете елемент чрез `[]`.
3. Конкатенирайте с `+` и изведете с `<<`.
4. Сравнете два масива с `==`.
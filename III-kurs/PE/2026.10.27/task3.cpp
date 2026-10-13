#include <iostream>
#include <limits>
#include <numeric>

const long long MAX_VALUE = 1000000;

class Fraction {
private:
    long long num;
    long long den;

    void reduce() {
        if (den == 0) den = 1;
        if (den < 0) {
            num = -num;
            den = -den;
        }
        long long g = std::gcd(num, den);
        num /= g;
        den /= g;
    }

public:
    Fraction(long long n = 0, long long d = 1) : num(n), den(d) {
        reduce();
    }

    Fraction add(const Fraction& f) const {
        long long g = std::gcd(den, f.den);
        return Fraction(num * (f.den / g) + f.num * (den / g), den / g * f.den);
    }

    Fraction add(int n) const {
        return Fraction(num + n * den, den);
    }

    void show() const {
        std::cout << num;
        if (den != 1) std::cout << '/' << den;
    }
};

bool readInt(const char* prompt, long long minValue, long long maxValue, int* value) {
    std::cout << prompt;
    long long v;
    while (!(std::cin >> v) || v < minValue || v > maxValue) {
        if (std::cin.eof()) return false;
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }
        std::cout << "Enter a whole number from " << minValue << " to " << maxValue << ": ";
    }
    *value = static_cast<int>(v);
    return true;
}

bool readFraction(const char* name, Fraction* f) {
    int n;
    int d;
    std::cout << "Fraction " << name << ":\n";
    if (!readInt("  numerator: ", -MAX_VALUE, MAX_VALUE, &n)) return false;
    while (true) {
        if (!readInt("  denominator (not 0): ", -MAX_VALUE, MAX_VALUE, &d)) return false;
        if (d != 0) break;
        std::cout << "  The denominator cannot be 0.\n";
    }
    *f = Fraction(n, d);
    return true;
}

void showSum(const Fraction& a, const Fraction& b, const Fraction& sum) {
    a.show();
    std::cout << " + ";
    b.show();
    std::cout << " = ";
    sum.show();
    std::cout << '\n';
}

void showSum(const Fraction& a, int n, const Fraction& sum) {
    a.show();
    std::cout << " + " << n << " = ";
    sum.show();
    std::cout << '\n';
}

int main() {
    Fraction half(1, 2);
    Fraction third(1, 3);
    Fraction s = half.add(third);
    showSum(half, third, s);
    showSum(s, 2, s.add(2));
    Fraction reduced(6, -8);
    std::cout << "Fraction(6, -8) is reduced to ";
    reduced.show();
    std::cout << "\n\n";

    Fraction a;
    Fraction b;
    int n;
    if (!readFraction("a", &a) || !readFraction("b", &b) || !readInt("Whole number n: ", -MAX_VALUE, MAX_VALUE, &n)) {
        std::cout << "\nInput ended\n";
        return 0;
    }

    std::cout << '\n';
    Fraction sum = a.add(b);
    showSum(a, b, sum);
    showSum(sum, n, sum.add(n));

    return 0;
}

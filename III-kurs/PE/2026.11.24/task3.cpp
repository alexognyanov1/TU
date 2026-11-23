#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

const int size = 4;
const float maxValue = 1000000.0f;

class Vec4 {
public:
    Vec4() : v{0.0f, 0.0f, 0.0f, 0.0f} {}
    Vec4(float a, float b, float c, float d) : v{a, b, c, d} {}

    float& operator[](int i) {
        check(i);
        return v[i];
    }

    const float& operator[](int i) const {
        check(i);
        return v[i];
    }

    friend Vec4 operator+(const Vec4& left, const Vec4& right);
    friend Vec4 operator-(const Vec4& left, const Vec4& right);
    friend Vec4 operator*(const Vec4& left, const Vec4& right);
    friend Vec4 operator/(const Vec4& left, const Vec4& right);

private:
    static void check(int i) {
        if (i < 0 || i >= size) {
            throw std::out_of_range("index " + std::to_string(i) + " is outside 0-3");
        }
    }

    float v[size];
};

Vec4 spread(float f) {
    return Vec4(f, f, f, f);
}

Vec4 operator+(const Vec4& left, const Vec4& right) {
    Vec4 result;
    for (int i = 0; i < size; ++i) {
        result.v[i] = left.v[i] + right.v[i];
    }
    return result;
}

Vec4 operator-(const Vec4& left, const Vec4& right) {
    Vec4 result;
    for (int i = 0; i < size; ++i) {
        result.v[i] = left.v[i] - right.v[i];
    }
    return result;
}

Vec4 operator*(const Vec4& left, const Vec4& right) {
    Vec4 result;
    for (int i = 0; i < size; ++i) {
        result.v[i] = left.v[i] * right.v[i];
    }
    return result;
}

Vec4 operator/(const Vec4& left, const Vec4& right) {
    Vec4 result;
    for (int i = 0; i < size; ++i) {
        if (right.v[i] == 0.0f) {
            throw std::domain_error("division by zero");
        }
        result.v[i] = left.v[i] / right.v[i];
    }
    return result;
}

Vec4 operator+(const Vec4& left, float right) {
    return left + spread(right);
}

Vec4 operator-(const Vec4& left, float right) {
    return left - spread(right);
}

Vec4 operator*(const Vec4& left, float right) {
    return left * spread(right);
}

Vec4 operator/(const Vec4& left, float right) {
    return left / spread(right);
}

Vec4 operator+(float left, const Vec4& right) {
    return spread(left) + right;
}

Vec4 operator-(float left, const Vec4& right) {
    return spread(left) - right;
}

Vec4 operator*(float left, const Vec4& right) {
    return spread(left) * right;
}

Vec4 operator/(float left, const Vec4& right) {
    return spread(left) / right;
}

void show(const std::string& name, const Vec4& vec) {
    std::cout << name << " = (";
    for (int i = 0; i < size; ++i) {
        std::cout << (i ? ", " : "") << vec[i];
    }
    std::cout << ")\n";
}

void showDivision(const std::string& name, const Vec4& left, const Vec4& right) {
    try {
        show(name, left / right);
    } catch (const std::domain_error& error) {
        std::cout << name << ": " << error.what() << '\n';
    }
}

void showAll(const Vec4& a, const Vec4& b, float f) {
    show("a + b", a + b);
    show("a - b", a - b);
    show("a * b", a * b);
    showDivision("a / b", a, b);
    show("a + f", a + f);
    show("a - f", a - f);
    show("a * f", a * f);
    showDivision("a / f", a, spread(f));
    show("f + a", f + a);
    show("f - a", f - a);
    show("f * a", f * a);
    showDivision("f / a", spread(f), a);
}

bool readNumbers(const std::string& prompt, int count, float low, float high, float values[]) {
    std::cout << prompt;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        bool valid = true;
        for (int i = 0; i < count && valid; ++i) {
            valid = (in >> values[i]) && values[i] >= low && values[i] <= high;
        }
        std::string extra;
        if (valid && !(in >> extra)) {
            return true;
        }
        std::cout << "Enter " << count << (count == 1 ? " number" : " numbers") << " from " << low << " to " << high << ": ";
    }
    return false;
}

bool readVec(const std::string& name, Vec4& vec) {
    float values[size];
    if (!readNumbers("Vector " + name + " (4 numbers): ", size, -maxValue, maxValue, values)) {
        return false;
    }
    for (int i = 0; i < size; ++i) {
        vec[i] = values[i];
    }
    return true;
}

bool readIndex(int& index) {
    std::cout << "Index of the element of a to double (0-3): ";
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        int i;
        char extra;
        if (in >> i && !(in >> extra)) {
            index = i;
            return true;
        }
        std::cout << "Enter a whole number: ";
    }
    return false;
}

int main() {
    Vec4 a(1.0f, 2.0f, 3.0f, 4.0f);
    Vec4 b(0.5f, 4.0f, -2.0f, 8.0f);
    float f = 2.0f;

    std::cout << "Vec4: a vector of four float\n";
    show("a", a);
    show("b", b);
    std::cout << "f = " << f << '\n';
    showAll(a, b, f);
    showDivision("a / 0", a, spread(0.0f));

    std::cout << "a[2] = " << a[2] << '\n';
    a[2] = 30.0f;
    show("a after a[2] = 30", a);
    const Vec4 fixed = a * b + f;
    std::cout << "(a * b + f)[3] = " << fixed[3] << '\n';
    try {
        a[4] = 1.0f;
    } catch (const std::out_of_range& error) {
        std::cout << "a[4]: " << error.what() << '\n';
    }

    std::cout << "\nYour vectors (numbers from " << -maxValue << " to " << maxValue << ")\n";
    float scalar[1];
    int index;
    if (!readVec("a", a) || !readVec("b", b) || !readNumbers("Number f: ", 1, -maxValue, maxValue, scalar)) {
        std::cout << "\nInput ended\n";
        return 0;
    }
    show("a", a);
    show("b", b);
    std::cout << "f = " << scalar[0] << '\n';
    showAll(a, b, scalar[0]);

    if (!readIndex(index)) {
        std::cout << "\nInput ended\n";
        return 0;
    }
    try {
        a[index] = a[index] * 2.0f;
        show("a", a);
    } catch (const std::out_of_range& error) {
        std::cout << "a[" << index << "]: " << error.what() << '\n';
    }
    return 0;
}

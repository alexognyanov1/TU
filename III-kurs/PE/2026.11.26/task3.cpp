#include <cmath>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

const int maxCount = 8;
const double maxValue = 1000000.0;

class DynArray {
public:
    explicit DynArray(int cap) : data(nullptr), size(0), capacity(cap) {
        if (cap < 0) {
            throw std::invalid_argument("the capacity cannot be negative");
        }
        data = new double[cap]();
    }

    DynArray(const DynArray& other) : data(new double[other.capacity]()), size(other.size), capacity(other.capacity) {
        for (int i = 0; i < size; ++i) {
            data[i] = other.data[i];
        }
    }

    ~DynArray() {
        delete[] data;
    }

    void push(double val) {
        if (size == capacity) {
            throw std::length_error("the array is full (capacity " + std::to_string(capacity) + ")");
        }
        data[size++] = val;
    }

    int length() const {
        return size;
    }

    double& operator[](int i) {
        check(i);
        return data[i];
    }

    const double& operator[](int i) const {
        check(i);
        return data[i];
    }

    DynArray& operator=(const DynArray& other) {
        if (this == &other) {
            return *this;
        }
        double* copy = new double[other.capacity]();
        for (int i = 0; i < other.size; ++i) {
            copy[i] = other.data[i];
        }
        delete[] data;
        data = copy;
        size = other.size;
        capacity = other.capacity;
        return *this;
    }

    DynArray operator+(const DynArray& other) const {
        DynArray result(capacity + other.capacity);
        for (int i = 0; i < size; ++i) {
            result.push(data[i]);
        }
        for (int i = 0; i < other.size; ++i) {
            result.push(other.data[i]);
        }
        return result;
    }

    bool operator==(const DynArray& other) const {
        if (size != other.size) {
            return false;
        }
        for (int i = 0; i < size; ++i) {
            if (data[i] != other.data[i]) {
                return false;
            }
        }
        return true;
    }

    friend std::ostream& operator<<(std::ostream& out, const DynArray& array);

private:
    void check(int i) const {
        if (i < 0 || i >= size) {
            throw std::out_of_range("index " + std::to_string(i) + " is outside the " + std::to_string(size) + " stored elements");
        }
    }

    double* data;
    int size;
    int capacity;
};

std::ostream& operator<<(std::ostream& out, const DynArray& array) {
    out << '[';
    for (int i = 0; i < array.size; ++i) {
        out << (i ? ", " : "") << array.data[i];
    }
    return out << ']';
}

const char* yesNo(bool value) {
    return value ? "true" : "false";
}

bool parseNumber(const std::string& text, double& value) {
    if (text.find_first_not_of("0123456789.eE+-") != std::string::npos) {
        return false;
    }
    char* end = nullptr;
    value = std::strtod(text.c_str(), &end);
    return end != text.c_str() && *end == '\0' && value >= -maxValue && value <= maxValue;
}

bool readArray(const std::string& name, DynArray& array) {
    std::cout << "Array " << name << " (0 to " << maxCount << " numbers on one line): ";
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        DynArray values(maxCount);
        std::string word;
        bool valid = true;
        while (valid && in >> word) {
            double value = 0.0;
            valid = values.length() < maxCount && parseNumber(word, value);
            if (valid) {
                values.push(value);
            }
        }
        if (valid) {
            array = values;
            return true;
        }
        std::cout << "Enter at most " << maxCount << " numbers from " << -maxValue << " to " << maxValue << ": ";
    }
    return false;
}

bool readChange(int& index, double& value) {
    std::cout << "Index and new value for a: ";
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        std::string word;
        std::string extra;
        int i = 0;
        char rest;
        if (in >> i && in.get(rest) && rest == ' ' && in >> word && !(in >> extra) && parseNumber(word, value)) {
            index = i;
            return true;
        }
        std::cout << "Enter a whole index and a number from " << -maxValue << " to " << maxValue << ": ";
    }
    return false;
}

void demo() {
    DynArray a(5);
    DynArray b(5);
    a.push(1.0);
    a.push(2.0);
    a.push(3.0);
    b.push(4.0);
    b.push(5.5);
    std::cout << "a = " << a << '\n';
    std::cout << "b = " << b << '\n';

    std::cout << "a[1] = " << a[1] << '\n';
    a[1] = 20.0;
    std::cout << "a after a[1] = 20: " << a << '\n';

    std::cout << "a + b = " << a + b << '\n';
    std::cout << "b + a = " << b + a << '\n';
    std::cout << "a == b: " << yesNo(a == b) << '\n';

    DynArray c(1);
    c = a;
    std::cout << "c = a: " << c << '\n';
    std::cout << "a == c: " << yesNo(a == c) << '\n';
    c[0] = 100.0;
    std::cout << "after c[0] = 100: c = " << c << ", a = " << a << '\n';
    std::cout << "a == c: " << yesNo(a == c) << '\n';

    DynArray& same = a;
    a = same;
    std::cout << "a after a = a: " << a << '\n';

    DynArray d(0);
    DynArray e(0);
    d = e = b;
    std::cout << "d = e = b: d = " << d << ", e = " << e << '\n';

    try {
        a[3] = 1.0;
    } catch (const std::out_of_range& error) {
        std::cout << "a[3]: " << error.what() << '\n';
    }
    try {
        DynArray small(1);
        small.push(1.0);
        small.push(2.0);
    } catch (const std::length_error& error) {
        std::cout << "second push into DynArray(1): " << error.what() << '\n';
    }
}

int main() {
    std::cout << "DynArray: a dynamic array of numbers\n";
    demo();

    std::cout << "\nYour arrays\n";
    DynArray a(maxCount);
    DynArray b(maxCount);
    int index = 0;
    double value = 0.0;
    if (!readArray("a", a) || !readArray("b", b)) {
        std::cout << "\nInput ended\n";
        return 0;
    }
    std::cout << "a = " << a << '\n';
    std::cout << "b = " << b << '\n';
    std::cout << "a + b = " << a + b << '\n';
    std::cout << "a == b: " << yesNo(a == b) << '\n';

    if (!readChange(index, value)) {
        std::cout << "\nInput ended\n";
        return 0;
    }
    try {
        a[index] = value;
        std::cout << "a = " << a << '\n';
    } catch (const std::out_of_range& error) {
        std::cout << "a[" << index << "]: " << error.what() << '\n';
    }
    std::cout << "a + b = " << a + b << '\n';
    std::cout << "a == b: " << yesNo(a == b) << '\n';
    return 0;
}

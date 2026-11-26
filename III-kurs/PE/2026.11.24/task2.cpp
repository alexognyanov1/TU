#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>

class RINT {
public:
    RINT(int v = 0) : value(v) {}

    int get() const {
        return value;
    }

    RINT operator+() const {
        return *this;
    }

    RINT operator-() const {
        return RINT(checked(-static_cast<long long>(value)));
    }

    friend RINT operator+(const RINT& left, const RINT& right);
    friend RINT operator-(const RINT& left, const RINT& right);
    friend RINT operator*(const RINT& left, const RINT& right);
    friend RINT operator/(const RINT& left, const RINT& right);

private:
    static int checked(long long result) {
        if (result < std::numeric_limits<int>::min() || result > std::numeric_limits<int>::max()) {
            throw std::overflow_error("the result does not fit in an int");
        }
        return static_cast<int>(result);
    }

    int value;
};

RINT operator+(const RINT& left, const RINT& right) {
    return RINT(RINT::checked(static_cast<long long>(left.value) + right.value));
}

RINT operator-(const RINT& left, const RINT& right) {
    return RINT(RINT::checked(static_cast<long long>(left.value) - right.value));
}

RINT operator*(const RINT& left, const RINT& right) {
    return RINT(RINT::checked(static_cast<long long>(left.value) * right.value));
}

RINT operator/(const RINT& left, const RINT& right) {
    if (right.value == 0) {
        throw std::domain_error("division by zero");
    }
    return RINT(RINT::checked(static_cast<long long>(left.value) / right.value));
}

bool parseInt(const std::string& text, int& value) {
    std::istringstream in(text);
    int v;
    char extra;
    if (in >> v && !(in >> extra)) {
        value = v;
        return true;
    }
    return false;
}

bool isSign(const std::string& text) {
    return text == "+" || text == "-";
}

bool isOperation(const std::string& text) {
    return isSign(text) || text == "*" || text == "/";
}

RINT calculate(const RINT& left, char operation, const RINT& right) {
    switch (operation) {
        case '+':
            return left + right;
        case '-':
            return left - right;
        case '*':
            return left * right;
        default:
            return left / right;
    }
}

bool evaluate(const std::string& line) {
    std::istringstream in(line);
    std::string tokens[4];
    int count = 0;
    while (count < 4 && in >> tokens[count]) {
        ++count;
    }
    int a;
    int b;
    try {
        if (count == 2 && isSign(tokens[0]) && parseInt(tokens[1], a)) {
            RINT x = a;
            RINT result = tokens[0] == "-" ? -x : +x;
            std::cout << tokens[0] << " (" << a << ") = " << result.get() << '\n';
            return true;
        }
        if (count == 3 && parseInt(tokens[0], a) && isOperation(tokens[1]) && parseInt(tokens[2], b)) {
            RINT x = a;
            RINT y = b;
            RINT result = calculate(x, tokens[1][0], y);
            std::cout << a << ' ' << tokens[1] << ' ' << b << " = " << result.get() << '\n';
            return true;
        }
    } catch (const std::exception& error) {
        std::cout << "Error: " << error.what() << '\n';
        return true;
    }
    return false;
}

int main() {
    RINT a = 17;
    RINT b(5);
    RINT c;

    std::cout << "RINT: an int with only +, -, * and /\n";
    std::cout << "a = " << a.get() << ", b = " << b.get() << ", c = " << c.get() << '\n';
    std::cout << "+a = " << (+a).get() << '\n';
    std::cout << "-a = " << (-a).get() << '\n';
    std::cout << "a + b = " << (a + b).get() << '\n';
    std::cout << "a - b = " << (a - b).get() << '\n';
    std::cout << "a * b = " << (a * b).get() << '\n';
    std::cout << "a / b = " << (a / b).get() << '\n';
    std::cout << "a + 3 = " << (a + 3).get() << '\n';
    std::cout << "3 - a = " << (3 - a).get() << '\n';
    c = -(a + b) * 2 / (b - 1);
    std::cout << "c = -(a + b) * 2 / (b - 1) = " << c.get() << '\n';
    try {
        c = a / (b - 5);
        std::cout << "a / (b - 5) = " << c.get() << '\n';
    } catch (const std::domain_error& error) {
        std::cout << "a / (b - 5): " << error.what() << '\n';
    }
    try {
        c = RINT(std::numeric_limits<int>::max()) + 1;
        std::cout << "max + 1 = " << c.get() << '\n';
    } catch (const std::overflow_error& error) {
        std::cout << "max + 1: " << error.what() << '\n';
    }

    const std::string help = "Enter a + b, a - b, a * b, a / b, + a or - a (separated by spaces), q to exit: ";
    std::cout << "\nCalculator with RINT\n" << help;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        std::string word;
        std::string extra;
        if (in >> word && word == "q" && !(in >> extra)) {
            std::cout << "Bye\n";
            return 0;
        }
        if (evaluate(line)) {
            std::cout << "Next expression or q: ";
        } else {
            std::cout << help;
        }
    }
    std::cout << "\nInput ended\n";
    return 0;
}

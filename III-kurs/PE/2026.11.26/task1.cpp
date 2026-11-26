#include <cmath>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

const double maxPart = 1000000.0;

bool parsePart(const std::string& text, double& value) {
    if (text.empty() || text.find_first_not_of("0123456789.eE+-") != std::string::npos) {
        return false;
    }
    char* end = nullptr;
    value = std::strtod(text.c_str(), &end);
    return end != text.c_str() && *end == '\0' && std::isfinite(value);
}

class Complex {
public:
    Complex(double r = 0.0, double i = 0.0) : real(r), imag(i) {}

    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }

    Complex operator-(const Complex& other) const {
        return Complex(real - other.real, imag - other.imag);
    }

    Complex operator*(const Complex& other) const {
        return Complex(real * other.real - imag * other.imag, real * other.imag + imag * other.real);
    }

    Complex operator/(const Complex& other) const {
        double divisor = other.real * other.real + other.imag * other.imag;
        if (divisor == 0.0) {
            throw std::domain_error("division by zero");
        }
        return Complex((real * other.real + imag * other.imag) / divisor, (imag * other.real - real * other.imag) / divisor);
    }

    Complex operator-() const {
        return Complex(-real, -imag);
    }

    bool operator==(const Complex& other) const {
        return real == other.real && imag == other.imag;
    }

    bool operator!=(const Complex& other) const {
        return !(*this == other);
    }

    double magnitude() const {
        return std::sqrt(real * real + imag * imag);
    }

    double getReal() const {
        return real;
    }

    double getImag() const {
        return imag;
    }

    friend std::ostream& operator<<(std::ostream& out, const Complex& number);
    friend std::istream& operator>>(std::istream& in, Complex& number);

private:
    double real;
    double imag;
};

std::ostream& operator<<(std::ostream& out, const Complex& number) {
    double shownReal = number.real == 0.0 ? 0.0 : number.real;
    return out << shownReal << (number.imag < 0.0 ? "-" : "+") << std::fabs(number.imag) << "i";
}

std::istream& operator>>(std::istream& in, Complex& number) {
    std::string text;
    if (!(in >> text)) {
        return in;
    }
    std::size_t split = std::string::npos;
    for (std::size_t i = 1; i + 1 < text.size(); ++i) {
        if ((text[i] == '+' || text[i] == '-') && text[i - 1] != 'e' && text[i - 1] != 'E') {
            split = i;
        }
    }
    double real = 0.0;
    double imag = 0.0;
    if (text.back() != 'i' || split == std::string::npos || !parsePart(text.substr(0, split), real) || !parsePart(text.substr(split, text.size() - split - 1), imag)) {
        in.setstate(std::ios::failbit);
        return in;
    }
    number.real = real;
    number.imag = imag;
    return in;
}

bool readComplex(const std::string& name, Complex& number) {
    std::cout << name << " (a+bi or a-bi): ";
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        Complex value;
        std::string extra;
        if (in >> value && !(in >> extra) && std::fabs(value.getReal()) <= maxPart && std::fabs(value.getImag()) <= maxPart) {
            number = value;
            return true;
        }
        std::cout << "Enter a number such as 3.5+2i or 3.5-2i, parts from " << -maxPart << " to " << maxPart << ": ";
    }
    return false;
}

int main() {
    std::cout << "Complex numbers\n";
    Complex z1;
    Complex z2;
    if (!readComplex("z1", z1) || !readComplex("z2", z2)) {
        std::cout << "\nInput ended\n";
        return 0;
    }

    std::cout << "z1 = " << z1 << '\n';
    std::cout << "z2 = " << z2 << '\n';
    std::cout << "z1 + z2 = " << z1 + z2 << '\n';
    std::cout << "z1 - z2 = " << z1 - z2 << '\n';
    std::cout << "z1 * z2 = " << z1 * z2 << '\n';
    try {
        Complex quotient = z1 / z2;
        std::cout << "z1 / z2 = " << quotient << '\n';
    } catch (const std::domain_error& error) {
        std::cout << "z1 / z2: " << error.what() << '\n';
    }
    std::cout << "-z1 = " << -z1 << '\n';
    std::cout << "(z1 + z2) * (-z1) = " << (z1 + z2) * (-z1) << '\n';
    std::cout << "|z1| = " << z1.magnitude() << '\n';
    std::cout << "|z2| = " << z2.magnitude() << '\n';
    std::cout << "z1 == z2: " << (z1 == z2 ? "true" : "false") << '\n';
    std::cout << "z1 != z2: " << (z1 != z2 ? "true" : "false") << '\n';
    return 0;
}

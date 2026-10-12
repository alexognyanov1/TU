#include <cstdlib>
#include <iostream>
#include <limits>

double readDouble(const char* prompt) {
    double value;
    std::cout << prompt;
    while (!(std::cin >> value)) {
        if (std::cin.eof()) {
            std::cout << "\nInput ended\n";
            std::exit(0);
        }
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Please enter a number: ";
    }
    return value;
}

class rectangle {
private:
    double a;
    double b;

public:
    rectangle() {
        do {
            std::cout << "\nEnter two positive values for the sides of the rectangle:\n";
            a = readDouble("a = ");
            b = readDouble("b = ");
        } while (!(a > 0 && b > 0));
    }

    double face() const {
        return a * b;
    }

    double face(double* p) const {
        *p = 2 * (a + b);
        return a * b;
    }

    void show(const char* name) const {
        std::cout << "Sides of the rectangle " << name << ":\n";
        std::cout << "a=" << a << ", b=" << b;
    }

    ~rectangle() {
        std::cout << "\nDestructing object rectangle!\n";
    }
};

int main() {
    rectangle r1;
    r1.show("r1");
    std::cout << "\nThe face of rectangle1 is s=" << r1.face() << '\n';

    rectangle r2;
    double p;
    r2.show("r2");
    double s = r2.face(&p);
    std::cout << "\nThe face of rectangle2 is s=" << s << ", and the perimeter is p=" << p << '\n';

    rectangle* pr = &r2;
    std::cout << "Through a pointer: s=" << pr->face() << '\n';

    return 0;
}

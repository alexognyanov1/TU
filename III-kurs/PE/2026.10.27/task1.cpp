#include <cmath>
#include <iostream>
#include <limits>

class Point {
private:
    double x;
    double y;

public:
    Point(double x = 0, double y = 0) : x(x), y(y) {}

    Point(const Point& p) : x(p.x), y(p.y) {
        std::cout << "Copying point\n";
    }

    void show() const {
        std::cout << "(" << x << ", " << y << ")\n";
    }

    friend double distance(Point a, Point b);
};

double distance(Point a, Point b) {
    return std::hypot(a.x - b.x, a.y - b.y);
}

bool readPoint(const char* name, double* x, double* y) {
    std::cout << "Въведете координати на точка " << name << ": ";
    while (!(std::cin >> *x >> *y)) {
        if (std::cin.eof()) {
            std::cout << "\nВходът свърши\n";
            return false;
        }
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Въведете две числа: ";
    }
    return true;
}

int main() {
    double x;
    double y;

    if (!readPoint("A", &x, &y)) return 0;
    Point a(x, y);
    if (!readPoint("B", &x, &y)) return 0;
    Point b(x, y);

    std::cout << "A";
    a.show();
    std::cout << "B";
    b.show();

    double d = distance(a, b);
    std::cout << "Разстоянието AB е " << d << '\n';

    return 0;
}

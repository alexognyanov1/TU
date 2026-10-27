#include <cmath>
#include <iostream>
#include <sstream>
#include <string>

class point {
private:
    double x;
    double y;

public:
    point(double xcoord, double ycoord);
    void print() const;
    static double dist(const point& p1, const point& p2);
    ~point();
};

point::point(double xcoord, double ycoord) : x(xcoord), y(ycoord) {
    std::cout << "Creating Point(" << x << "," << y << ")\n";
}

void point::print() const {
    std::cout << "Point(" << x << "," << y << ")";
}

double point::dist(const point& p1, const point& p2) {
    return std::sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y));
}

point::~point() {
    std::cout << "Destructing ";
    print();
    std::cout << '\n';
}

double distByValue(point p1, point p2) {
    return point::dist(p1, p2);
}

void printDistance(const point& p1, const point& p2) {
    std::cout << "Distance between ";
    p1.print();
    std::cout << " and ";
    p2.print();
    std::cout << " is " << point::dist(p1, p2) << '\n';
}

bool readPoint(const std::string& prompt, double& x, double& y) {
    std::cout << prompt;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        char extra;
        if (in >> x >> y && !(in >> extra) && std::isfinite(x) && std::isfinite(y)) return true;
        std::cout << "Enter two numbers separated by a space: ";
    }
    return false;
}

int main() {
    point a(3, 4);
    point b(10, 4);
    printDistance(a, b);

    std::cout << "\nBy value the points are copied, and the copies are destructed too:\n";
    double d = distByValue(a, b);
    std::cout << "Distance (by value) is " << d << '\n';

    std::cout << "\nEnter your own points\n";
    double x1;
    double y1;
    double x2;
    double y2;
    if (!readPoint("First point (x y): ", x1, y1) || !readPoint("Second point (x y): ", x2, y2)) {
        std::cout << "\nInput ended\n";
        return 0;
    }
    point p(x1, y1);
    point q(x2, y2);
    printDistance(p, q);

    return 0;
}

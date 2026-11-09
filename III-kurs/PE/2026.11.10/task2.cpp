#include <iostream>
#include <sstream>
#include <string>

class area {
    double dim1 = 0;
    double dim2 = 0;

public:
    virtual ~area() = default;

    void setarea(double d1, double d2) {
        dim1 = d1;
        dim2 = d2;
    }

    void getdim(double& d1, double& d2) const {
        d1 = dim1;
        d2 = dim2;
    }

    virtual double getarea() const = 0;
};

class rectangle : public area {
public:
    double getarea() const override {
        double d1;
        double d2;
        getdim(d1, d2);
        return d1 * d2;
    }
};

class triangle : public area {
public:
    double getarea() const override {
        double d1;
        double d2;
        getdim(d1, d2);
        return 0.5 * d1 * d2;
    }
};

bool readInt(const std::string& prompt, int low, int high, int& value) {
    std::cout << prompt;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        int v;
        char extra;
        if (in >> v && !(in >> extra) && v >= low && v <= high) {
            value = v;
            return true;
        }
        std::cout << "Enter a whole number from " << low << " to " << high << ": ";
    }
    return false;
}

bool readSize(const std::string& prompt, double& value) {
    const double maxSize = 10000;
    std::cout << prompt;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        double v;
        char extra;
        if (in >> v && !(in >> extra) && v > 0 && v <= maxSize) {
            value = v;
            return true;
        }
        std::cout << "Enter a number greater than 0 and at most " << maxSize << ": ";
    }
    return false;
}

void printArea(const area& a, const std::string& name) {
    std::cout << name << " has area: " << a.getarea() << '\n';
}

int main() {
    area* p;
    rectangle r;
    triangle t;
    r.setarea(3.3, 4.5);
    t.setarea(4.0, 5.0);
    p = &r;
    std::cout << "Rectangle has area: " << p->getarea() << '\n';
    p = &t;
    std::cout << "Triangle has area: " << p->getarea() << '\n';

    int choice;
    while (readInt("\nShape (1 - rectangle, 2 - triangle, 0 - exit): ", 0, 2, choice)) {
        if (choice == 0) {
            std::cout << "Bye\n";
            return 0;
        }
        double d1;
        double d2;
        if (!readSize(choice == 1 ? "Width: " : "Base: ", d1)
                || !readSize(choice == 1 ? "Height: " : "Height to the base: ", d2)) {
            break;
        }
        if (choice == 1) {
            r.setarea(d1, d2);
            p = &r;
            printArea(*p, "Rectangle");
        } else {
            t.setarea(d1, d2);
            p = &t;
            printArea(*p, "Triangle");
        }
    }
    std::cout << "\nInput ended\n";
    return 0;
}

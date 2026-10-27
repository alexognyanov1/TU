#include <iostream>
#include <sstream>
#include <string>

class vehicle {
    int num_wheels;
    int range;

public:
    vehicle(int w, int r) : num_wheels(w), range(r) {}

    void showv() const {
        std::cout << "Wheels:" << num_wheels << '\n';
        std::cout << "Range:" << range << '\n';
    }
};

class car : public vehicle {
    int passengers;

public:
    car(int p, int w, int r) : vehicle(w, r), passengers(p) {}

    void show() const {
        showv();
        std::cout << "Passengers:" << passengers << '\n';
    }
};

class truck : public vehicle {
    int loadlimit;

public:
    truck(int l, int w, int r) : vehicle(w, r), loadlimit(l) {}

    void show() const {
        showv();
        std::cout << "Loadlimit:" << loadlimit << '\n';
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

int main() {
    car c(5, 4, 500);
    truck t(30000, 12, 1200);
    std::cout << "Car:\n";
    c.show();
    std::cout << "\nTruck:\n";
    t.show();

    int passengers;
    int carWheels;
    int carRange;
    int loadlimit;
    int truckWheels;
    int truckRange;
    std::cout << "\nEnter your own car\n";
    if (!readInt("Passengers (1-50): ", 1, 50, passengers) || !readInt("Wheels (2-30): ", 2, 30, carWheels)
            || !readInt("Range (1-10000): ", 1, 10000, carRange)) {
        std::cout << "\nInput ended\n";
        return 0;
    }
    std::cout << "\nEnter your own truck\n";
    if (!readInt("Load limit (1-100000): ", 1, 100000, loadlimit) || !readInt("Wheels (2-30): ", 2, 30, truckWheels)
            || !readInt("Range (1-10000): ", 1, 10000, truckRange)) {
        std::cout << "\nInput ended\n";
        return 0;
    }
    car myCar(passengers, carWheels, carRange);
    truck myTruck(loadlimit, truckWheels, truckRange);
    std::cout << "\nYour car:\n";
    myCar.show();
    std::cout << "\nYour truck:\n";
    myTruck.show();

    return 0;
}

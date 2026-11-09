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

enum motor { gas, electric, diesel };

class motorized : virtual public vehicle {
    motor mtr;

public:
    motorized(motor m, int w, int r) : vehicle(w, r), mtr(m) {}

    void showm() const {
        std::cout << "Motor:";
        switch (mtr) {
            case gas:
                std::cout << "Gas\n";
                break;
            case electric:
                std::cout << "Electric\n";
                break;
            case diesel:
                std::cout << "Diesel\n";
                break;
        }
    }
};

class road_use : virtual public vehicle {
    int passengers;

public:
    road_use(int p, int w, int r) : vehicle(w, r), passengers(p) {}

    void showr() const {
        std::cout << "Passengers:" << passengers << '\n';
    }
};

enum steering { power, rack_pinion, manual };

class car : public motorized, public road_use {
    steering strng;

public:
    car(steering s, motor m, int p, int w, int r) : vehicle(w, r), motorized(m, w, r), road_use(p, w, r), strng(s) {}

    void show() const {
        showv();
        showr();
        showm();
        std::cout << "Steering: ";
        switch (strng) {
            case power:
                std::cout << "Power\n";
                break;
            case rack_pinion:
                std::cout << "Rack and pinion\n";
                break;
            case manual:
                std::cout << "Manual\n";
                break;
        }
    }
};

void showAsVehicle(const vehicle& v) {
    std::cout << "As a vehicle (one shared vehicle base):\n";
    v.showv();
}

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
    car c(power, gas, 5, 4, 500);
    c.show();
    showAsVehicle(c);

    int s;
    int m;
    int p;
    int w;
    int r;
    std::cout << "\nEnter your own car\n";
    if (!readInt("Steering (1 - Power, 2 - Rack and pinion, 3 - Manual): ", 1, 3, s)
            || !readInt("Motor (1 - Gas, 2 - Electric, 3 - Diesel): ", 1, 3, m)
            || !readInt("Passengers (1-50): ", 1, 50, p) || !readInt("Wheels (2-30): ", 2, 30, w)
            || !readInt("Range (1-10000): ", 1, 10000, r)) {
        std::cout << "\nInput ended\n";
        return 0;
    }
    car mine(static_cast<steering>(s - 1), static_cast<motor>(m - 1), p, w, r);
    std::cout << "\nYour car:\n";
    mine.show();
    showAsVehicle(mine);

    return 0;
}

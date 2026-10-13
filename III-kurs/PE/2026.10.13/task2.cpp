#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>

namespace standalone {

class truck;

class car {
    int passengers;
    int speed;

public:
    car(int p, int s) : passengers(p), speed(s > 0 ? s : 1) {}

    int getPassengers() const { return passengers; }

    friend int sp_greater(car c, truck t);
    friend double travel_time(car c, truck t, double km, double* truck_hours);
};

class truck {
    int weight;
    int speed;

public:
    truck(int w, int s) : weight(w), speed(s > 0 ? s : 1) {}

    int getWeight() const { return weight; }

    friend int sp_greater(car c, truck t);
    friend double travel_time(car c, truck t, double km, double* truck_hours);
};

int sp_greater(car c, truck t) {
    return c.speed - t.speed;
}

double travel_time(car c, truck t, double km, double* truck_hours) {
    *truck_hours = km / t.speed;
    return km / c.speed;
}

}

namespace member {

class truck;

class car {
    int passengers;
    int speed;

public:
    car(int p, int s) : passengers(p), speed(s > 0 ? s : 1) {}

    int getPassengers() const { return passengers; }

    int sp_greater(truck t);
    double travel_time(truck t, double km, double* truck_hours);
};

class truck {
    int weight;
    int speed;

public:
    truck(int w, int s) : weight(w), speed(s > 0 ? s : 1) {}

    int getWeight() const { return weight; }

    friend int car::sp_greater(truck t);
    friend double car::travel_time(truck t, double km, double* truck_hours);
};

int car::sp_greater(truck t) {
    return speed - t.speed;
}

double car::travel_time(truck t, double km, double* truck_hours) {
    *truck_hours = km / t.speed;
    return km / speed;
}

}

double readDistance() {
    double km;
    std::cout << "Enter distance in km (S > 0): ";
    while (!(std::cin >> km) || !(km > 0)) {
        if (std::cin.eof()) {
            std::cout << "\nInput ended\n";
            std::exit(0);
        }
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }
        std::cout << "Distance must be a positive number: ";
    }
    return km;
}

void printComparison(const char* carName, int passengers, const char* truckName, int weight, int t) {
    std::cout << "Comparing " << carName << " (" << passengers << " passengers) and "
        << truckName << " (" << weight << " kg):\n";
    if (t < 0) std::cout << "Truck is faster.\n";
    else if (t == 0) std::cout << "Car and truck speed is the same.\n";
    else std::cout << "Car is faster.\n";
}

void printTimes(double km, double carHours, double truckHours) {
    std::cout << "T = S / V for S=" << km << " km: car " << carHours << " h, truck " << truckHours << " h\n";
    if (carHours < truckHours) std::cout << "The car arrives " << truckHours - carHours << " h earlier.\n";
    else if (carHours > truckHours) std::cout << "The truck arrives " << carHours - truckHours << " h earlier.\n";
    else std::cout << "They arrive at the same time.\n";
}

int main() {
    double km = readDistance();
    std::cout << std::fixed << std::setprecision(2);
    double carHours;
    double truckHours;

    std::cout << "\n--- Friend function of both classes ---\n";
    standalone::car c1(6, 55), c2(2, 120);
    standalone::truck t1(10000, 55), t2(20000, 72);

    printComparison("c1", c1.getPassengers(), "t1", t1.getWeight(), sp_greater(c1, t1));
    carHours = travel_time(c1, t1, km, &truckHours);
    printTimes(km, carHours, truckHours);

    std::cout << "\n";
    printComparison("c2", c2.getPassengers(), "t2", t2.getWeight(), sp_greater(c2, t2));
    carHours = travel_time(c2, t2, km, &truckHours);
    printTimes(km, carHours, truckHours);

    std::cout << "\n--- Member function of car, friend of truck ---\n";
    member::car m1(6, 55), m2(2, 120);
    member::truck u1(10000, 55), u2(20000, 72);

    printComparison("c1", m1.getPassengers(), "t1", u1.getWeight(), m1.sp_greater(u1));
    carHours = m1.travel_time(u1, km, &truckHours);
    printTimes(km, carHours, truckHours);

    std::cout << "\n";
    printComparison("c2", m2.getPassengers(), "t2", u2.getWeight(), m2.sp_greater(u2));
    carHours = m2.travel_time(u2, km, &truckHours);
    printTimes(km, carHours, truckHours);

    return 0;
}

#include <iomanip>
#include <iostream>
#include <limits>

class Time {
private:
    int hours;
    int minutes;
    int seconds;

public:
    Time() : hours(0), minutes(0), seconds(0) {}

    bool setHours(int h) {
        if (h < 0 || h > 23) return false;
        hours = h;
        return true;
    }

    bool setMinutes(int m) {
        if (m < 0 || m > 59) return false;
        minutes = m;
        return true;
    }

    bool setSeconds(int s) {
        if (s < 0 || s > 59) return false;
        seconds = s;
        return true;
    }

    bool setTime(int h, int m, int s) {
        if (h < 0 || h > 23 || m < 0 || m > 59 || s < 0 || s > 59) return false;
        hours = h;
        minutes = m;
        seconds = s;
        return true;
    }

    void print24() const {
        std::cout << std::setfill('0') << std::setw(2) << hours << ':'
                  << std::setw(2) << minutes << ':'
                  << std::setw(2) << seconds << '\n';
    }

    void print12() const {
        int h = hours % 12;
        if (h == 0) h = 12;
        std::cout << std::setfill('0') << std::setw(2) << h << ':'
                  << std::setw(2) << minutes << ':'
                  << std::setw(2) << seconds << (hours < 12 ? " AM" : " PM") << '\n';
    }
};

int readInt(const char* prompt) {
    int value;
    std::cout << prompt;
    while (!(std::cin >> value)) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Please enter a whole number: ";
    }
    return value;
}

int main() {
    Time t;

    while (true) {
        int h = readInt("Hours (0-23): ");
        int m = readInt("Minutes (0-59): ");
        int s = readInt("Seconds (0-59): ");
        if (t.setTime(h, m, s)) break;
        std::cout << "Invalid time, try again.\n";
    }

    std::cout << "24-hour format: ";
    t.print24();
    std::cout << "12-hour format: ";
    t.print12();

    Time noon;
    noon.setHours(12);
    noon.setMinutes(0);
    noon.setSeconds(0);
    std::cout << "Noon: ";
    noon.print12();

    if (!noon.setMinutes(75)) {
        std::cout << "setMinutes(75) rejected, time stays ";
        noon.print24();
    }

    return 0;
}

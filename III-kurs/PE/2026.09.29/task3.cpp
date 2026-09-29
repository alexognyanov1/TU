#include <chrono>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <thread>

class Line {
private:
    int Len;

public:
    Line(int length) : Len(length > 0 ? length : 0) {
        for (int i = 0; i < Len; i++) std::cout << '*';
        std::cout << std::flush;
    }

    ~Line() {
        for (int i = 0; i < Len; i++) std::cout << '\b';
        for (int i = 0; i < Len; i++) std::cout << ' ';
        for (int i = 0; i < Len; i++) std::cout << '\b';
        std::cout << std::flush;
    }
};

int readLength() {
    int value;
    std::cout << "Line length: ";
    while (!(std::cin >> value) || value < 0) {
        if (std::cin.eof()) {
            std::cout << "\nInput ended\n";
            std::exit(0);
        }
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Length must be a whole number, 0 or more: ";
    }
    return value;
}

int main() {
    int length = readLength();

    {
        Line line(length);
        std::this_thread::sleep_for(std::chrono::seconds(2));
    }

    std::cout << "Line erased (length was " << length << ")\n";
    return 0;
}

#include <chrono>
#include <iostream>
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

int main() {
    int length;
    std::cout << "Line length: ";
    std::cin >> length;

    {
        Line line(length);
        std::this_thread::sleep_for(std::chrono::seconds(2));
    }

    std::cout << "Line erased (length was " << length << ")\n";
    return 0;
}

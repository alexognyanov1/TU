#include <iostream>
#include <limits>

class pr2;

class pr1 {
    int printing;

public:
    pr1() { printing = 0; }
    void set_print(int status) { printing = status; }

    friend bool inuse(const pr1& a, const pr2& b);
};

class pr2 {
    int printing;

public:
    pr2() { printing = 0; }
    void set_print(int status) { printing = status; }

    friend bool inuse(const pr1& a, const pr2& b);
};

bool inuse(const pr1& a, const pr2& b) {
    return a.printing != 0 || b.printing != 0;
}

void report(const char* step, const pr1& a, const pr2& b) {
    std::cout << step << " -> printer " << (inuse(a, b) ? "is in use" : "is free") << '\n';
}

bool readStatus(const char* prompt, int* status) {
    std::cout << prompt;
    while (!(std::cin >> *status) || (*status != 0 && *status != 1)) {
        if (std::cin.eof()) return false;
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }
        std::cout << "Status must be 0 (idle) or 1 (printing): ";
    }
    return true;
}

int main() {
    pr1 a;
    pr2 b;

    report("Start", a, b);
    a.set_print(1);
    report("pr1 starts printing", a, b);
    a.set_print(0);
    report("pr1 finishes", a, b);
    b.set_print(1);
    report("pr2 starts printing", a, b);
    a.set_print(1);
    report("pr1 also printing", a, b);
    a.set_print(0);
    b.set_print(0);
    report("Both finish", a, b);

    std::cout << "\nEnter statuses (0/1) for pr1 and pr2, end with Ctrl+D:\n";
    pr1* pa = &a;
    pr2* pb = &b;
    int s1;
    int s2;
    while (readStatus("pr1: ", &s1) && readStatus("pr2: ", &s2)) {
        pa->set_print(s1);
        pb->set_print(s2);
        report("inuse()", *pa, *pb);
    }
    std::cout << "\nInput ended\n";

    return 0;
}

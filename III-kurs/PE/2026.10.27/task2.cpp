#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

class array {
    int size;
    char* p;

    void check(int i) const {
        if (i < 0 || i >= size) {
            throw std::out_of_range("Bounds error!!! Index " + std::to_string(i) + " is outside 0.."
                    + std::to_string(size - 1));
        }
    }

public:
    explicit array(int num);
    array(const array&) = delete;
    array& operator=(const array&) = delete;
    ~array() { delete[] p; }

    char& put(int i);
    char get(int i) const;
    int length() const { return size; }
};

array::array(int num) : size(num > 0 ? num : 1), p(new char[size]) {
    for (int i = 0; i < size; ++i) p[i] = '.';
}

char& array::put(int i) {
    check(i);
    return p[i];
}

char array::get(int i) const {
    check(i);
    return p[i];
}

void show(const array& a) {
    std::cout << "Contents:";
    for (int i = 0; i < a.length(); ++i) std::cout << ' ' << a.get(i);
    std::cout << '\n';
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
    array a(10);
    a.put(3) = 'X';
    a.put(2) = 'R';
    std::cout << a.get(3) << "\n" << a.get(2);
    std::cout << "\n";
    try {
        a.put(11) = '!';
    } catch (const std::out_of_range& e) {
        std::cout << e.what() << '\n';
    }
    show(a);

    int n;
    if (!readInt("\nSize of your array (1-100): ", 1, 100, n)) {
        std::cout << "\nInput ended\n";
        return 0;
    }
    array b(n);
    std::cout << "Commands: put INDEX CHAR, get INDEX, show\n";
    std::string line;
    std::cout << "> ";
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        std::string command;
        int i;
        char c;
        char extra;
        in >> command;
        try {
            if (command == "put" && in >> i >> c && !(in >> extra)) {
                b.put(i) = c;
                std::cout << "Stored " << c << " at " << i << '\n';
            } else if (command == "get" && in >> i && !(in >> extra)) {
                c = b.get(i);
                std::cout << "At " << i << ": " << c << '\n';
            } else if (command == "show" && !(in >> extra)) {
                show(b);
            } else if (!command.empty()) {
                std::cout << "Use: put INDEX CHAR, get INDEX or show\n";
            }
        } catch (const std::out_of_range& e) {
            std::cout << e.what() << '\n';
        }
        std::cout << "> ";
    }
    std::cout << "\nInput ended\n";
    show(b);

    return 0;
}

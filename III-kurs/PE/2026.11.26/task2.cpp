#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>

const int mapCapacity = 8;
const int bufferCapacity = 5;
const double maxNumber = 1000000.0;

class BankAccount {
public:
    BankAccount(const std::string& name, double start) : owner(name), balance(start < 0.0 ? 0.0 : start) {}

    ~BankAccount() {
        std::cout << "[BankAccount] the account of " << owner << " is deleted\n";
    }

    void deposit(double amount) {
        if (!(amount > 0.0) || amount > maxNumber) {
            throw std::invalid_argument("the amount must be above 0 and at most 1000000");
        }
        balance += amount;
    }

    void describe() const {
        std::cout << owner << ": " << balance << " lv\n";
    }

private:
    std::string owner;
    double balance;
};

template <typename T>
class LoggedPtr {
public:
    explicit LoggedPtr(T* raw = nullptr) : pointer(raw) {}

    LoggedPtr(const LoggedPtr&) = delete;

    ~LoggedPtr() {
        delete pointer;
    }

    LoggedPtr& operator=(LoggedPtr&& other) noexcept {
        if (this != &other) {
            delete pointer;
            pointer = other.pointer;
            other.pointer = nullptr;
        }
        return *this;
    }

    T* operator->() {
        check();
        std::cout << "[LoggedPtr] -> access\n";
        return pointer;
    }

    T& operator*() {
        check();
        return *pointer;
    }

    bool isNull() const {
        return pointer == nullptr;
    }

private:
    void check() const {
        if (pointer == nullptr) {
            throw std::logic_error("the pointer is nullptr");
        }
    }

    T* pointer;
};

class ConfigMap {
public:
    ConfigMap() : count(0) {}

    ConfigMap(const ConfigMap& other) : count(0) {
        copyFrom(other);
    }

    std::string& operator[](const std::string& key) {
        for (int i = 0; i < count; ++i) {
            if (keys[i] == key) {
                return values[i];
            }
        }
        if (count == mapCapacity) {
            throw std::length_error("the map is full (" + std::to_string(mapCapacity) + " keys)");
        }
        keys[count] = key;
        values[count].clear();
        return values[count++];
    }

    ConfigMap& operator=(const ConfigMap& other) {
        if (this != &other) {
            copyFrom(other);
        }
        return *this;
    }

    friend std::ostream& operator<<(std::ostream& out, const ConfigMap& map);

private:
    void copyFrom(const ConfigMap& other) {
        count = other.count;
        for (int i = 0; i < count; ++i) {
            keys[i] = other.keys[i];
            values[i] = other.values[i];
        }
    }

    std::string keys[mapCapacity];
    std::string values[mapCapacity];
    int count;
};

std::ostream& operator<<(std::ostream& out, const ConfigMap& map) {
    if (map.count == 0) {
        out << "(empty map)\n";
    }
    for (int i = 0; i < map.count; ++i) {
        out << map.keys[i] << " = " << map.values[i] << '\n';
    }
    return out;
}

class CircularBuffer {
public:
    explicit CircularBuffer(int cap) : data(nullptr), capacity(cap), count(0), next(0) {
        if (cap < 1) {
            throw std::invalid_argument("the capacity must be at least 1");
        }
        data = new double[cap]();
    }

    CircularBuffer(const CircularBuffer& other) : data(new double[other.capacity]()), capacity(other.capacity), count(other.count), next(other.next) {
        for (int i = 0; i < capacity; ++i) {
            data[i] = other.data[i];
        }
    }

    ~CircularBuffer() {
        delete[] data;
    }

    void push(double value) {
        data[next] = value;
        next = (next + 1) % capacity;
        if (count < capacity) {
            ++count;
        }
    }

    int size() const {
        return count;
    }

    double& operator[](int i) {
        return data[physical(i)];
    }

    const double& operator[](int i) const {
        return data[physical(i)];
    }

    CircularBuffer& operator=(const CircularBuffer& other) {
        if (this == &other) {
            return *this;
        }
        double* copy = new double[other.capacity]();
        for (int i = 0; i < other.capacity; ++i) {
            copy[i] = other.data[i];
        }
        delete[] data;
        data = copy;
        capacity = other.capacity;
        count = other.count;
        next = other.next;
        return *this;
    }

    friend std::ostream& operator<<(std::ostream& out, const CircularBuffer& buffer);

private:
    int physical(int i) const {
        if (i < 0 || i >= count) {
            throw std::out_of_range("index " + std::to_string(i) + " is outside the " + std::to_string(count) + " stored elements");
        }
        return (next - 1 - i + capacity) % capacity;
    }

    double* data;
    int capacity;
    int count;
    int next;
};

std::ostream& operator<<(std::ostream& out, const CircularBuffer& buffer) {
    out << '[';
    for (int i = 0; i < buffer.count; ++i) {
        out << (i ? ", " : "") << buffer[i];
    }
    return out << ']';
}

void demoLoggedPtr() {
    std::cout << "LoggedPtr\n";
    LoggedPtr<BankAccount> p(new BankAccount("Ivan", 1000.0));
    p->deposit(500.0);
    p->describe();
    std::cout << "(*p).describe(): ";
    (*p).describe();

    LoggedPtr<BankAccount> q(new BankAccount("Maria", 20.0));
    std::cout << "q = std::move(p)\n";
    q = std::move(p);
    std::cout << "p is nullptr: " << (p.isNull() ? "yes" : "no") << ", q is nullptr: " << (q.isNull() ? "yes" : "no") << '\n';
    q->describe();
    try {
        p->describe();
    } catch (const std::logic_error& error) {
        std::cout << "p->describe(): " << error.what() << '\n';
    }
    std::cout << "end of the scope of q\n";
}

void demoConfigMap() {
    std::cout << "\nConfigMap\n";
    ConfigMap cfg;
    cfg["host"] = "localhost";
    cfg["port"] = "5432";
    cfg["db"] = "mydb";
    std::cout << cfg;

    cfg["port"] = "5433";
    std::cout << "port after cfg[\"port\"] = \"5433\": " << cfg["port"] << '\n';
    std::cout << "missing key user: \"" << cfg["user"] << "\"\n";

    ConfigMap copy;
    ConfigMap other;
    other = copy = cfg;
    copy["host"] = "example.org";
    std::cout << "copy after copy[\"host\"] = \"example.org\":\n" << copy;
    std::cout << "the original:\n" << cfg;
    std::cout << "other[\"db\"]: " << other["db"] << '\n';
}

void demoCircularBuffer() {
    std::cout << "\nCircularBuffer\n";
    CircularBuffer buf(bufferCapacity);
    for (int i = 1; i <= 7; ++i) {
        buf.push(i);
    }
    std::cout << "after pushing 1 to 7 into capacity 5: " << buf << '\n';
    std::cout << "buf[0] = " << buf[0] << ", expected 7: " << (buf[0] == 7.0 ? "correct" : "wrong") << '\n';
    std::cout << "buf[4] = " << buf[4] << ", expected 3: " << (buf[4] == 3.0 ? "correct" : "wrong") << '\n';

    CircularBuffer copy(1);
    copy = buf;
    buf[0] = 70.0;
    std::cout << "after buf[0] = 70: " << buf << '\n';
    std::cout << "the copy made before it: " << copy << '\n';
    try {
        buf[5] = 1.0;
    } catch (const std::out_of_range& error) {
        std::cout << "buf[5]: " << error.what() << '\n';
    }
}

bool readNumber(std::istringstream& in, double& value) {
    std::string extra;
    return in >> value && !(in >> extra) && value >= -maxNumber && value <= maxNumber;
}

void help() {
    std::cout << "Commands: deposit AMOUNT | set KEY VALUE | get KEY | push NUMBER | at INDEX | show | q\n";
}

int main() {
    demoLoggedPtr();
    demoConfigMap();
    demoCircularBuffer();

    std::cout << "\nYour turn\n";
    LoggedPtr<BankAccount> account(new BankAccount("Student", 0.0));
    ConfigMap cfg;
    CircularBuffer buf(bufferCapacity);
    help();

    std::string line;
    while (std::cout << "> " && std::getline(std::cin, line)) {
        std::istringstream in(line);
        std::string command;
        std::string key;
        std::string value;
        std::string extra;
        double number = 0.0;
        int index = 0;
        in >> command;
        try {
            if (command == "q" && !(in >> extra)) {
                std::cout << "Bye\n";
                return 0;
            } else if (command == "deposit" && readNumber(in, number)) {
                account->deposit(number);
                (*account).describe();
            } else if (command == "set" && in >> key >> value && !(in >> extra)) {
                cfg[key] = value;
                std::cout << cfg;
            } else if (command == "get" && in >> key && !(in >> extra)) {
                std::string& found = cfg[key];
                std::cout << key << " = \"" << found << "\"\n";
            } else if (command == "push" && readNumber(in, number)) {
                buf.push(number);
                std::cout << buf << '\n';
            } else if (command == "at" && in >> index && !(in >> extra)) {
                double element = buf[index];
                std::cout << "buf[" << index << "] = " << element << '\n';
            } else if (command == "show" && !(in >> extra)) {
                (*account).describe();
                std::cout << cfg << buf << '\n';
            } else {
                help();
            }
        } catch (const std::exception& error) {
            std::cout << "Error: " << error.what() << '\n';
        }
    }
    std::cout << "\nInput ended\n";
    return 0;
}

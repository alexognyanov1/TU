#include <cstring>
#include <iostream>
#include <sstream>
#include <string>

enum ZooLocs { ZOOANIMAL, BEAR, PANDA, TIGER, ELEPHANT };

const char* const locTable[] = {
    "Whole zoo area",
    "North B1: brown area",
    "East B1,P area",
    "South T1: tiger area",
    "West E1: elephant house"
};

const int maxAdded = 20;
const std::size_t maxNameLength = 30;

char* copyText(const char* s) {
    char* text = new char[std::strlen(s) + 1];
    std::strcpy(text, s);
    return text;
}

class ZooAnimal {
    friend void print(const ZooAnimal* pz);

public:
    ZooAnimal(const char* s = "ZooAnimal") : name(copyText(s)), next(nullptr) {}
    ZooAnimal(const ZooAnimal&) = delete;
    ZooAnimal& operator=(const ZooAnimal&) = delete;
    virtual ~ZooAnimal() { delete[] name; }
    void link(ZooAnimal* za);
    virtual void print() const;
    virtual void isA() const;

protected:
    char* name;
    ZooAnimal* next;
};

class Bear : public ZooAnimal {
public:
    Bear(const char* s = "Bear", ZooLocs loc = BEAR, const char* sci = "Ursidae");
    ~Bear() override { delete[] sciName; }
    void print() const override;
    void isA() const override;

protected:
    char* sciName;
    ZooLocs ZooArea;
};

class Panda : public Bear {
public:
    Panda(const char* nm, int room, const char* s = "Panda", const char* sci = "Ailuropoda Melaoleuca",
            ZooLocs loc = PANDA);
    ~Panda() override { delete[] indName; }
    void print() const override;
    void isA() const override;

protected:
    char* indName;
    int cell;
};

class Tiger : public ZooAnimal {
public:
    Tiger(const char* nm, int enclosure, const char* s = "Tiger", const char* sci = "Panthera tigris",
            ZooLocs loc = TIGER);
    ~Tiger() override;
    void print() const override;
    void isA() const override;

protected:
    char* sciName;
    char* indName;
    ZooLocs ZooArea;
    int enclosureNo;
};

class Elephant : public ZooAnimal {
public:
    Elephant(const char* nm, int kg, const char* s = "Elephant", const char* sci = "Loxodonta africana",
            ZooLocs loc = ELEPHANT);
    ~Elephant() override;
    void print() const override;
    void isA() const override;

protected:
    char* sciName;
    char* indName;
    ZooLocs ZooArea;
    int weight;
};

void ZooAnimal::link(ZooAnimal* za) {
    za->next = next;
    next = za;
}

void ZooAnimal::isA() const {
    std::cout << "Animal name: " << name << '\n';
}

void ZooAnimal::print() const {
    isA();
}

Bear::Bear(const char* s, ZooLocs loc, const char* sci) : ZooAnimal(s), sciName(copyText(sci)), ZooArea(loc) {}

void Bear::isA() const {
    ZooAnimal::isA();
    std::cout << "\tSname: \t" << sciName << '\n';
}

void Bear::print() const {
    ZooAnimal::print();
    std::cout << "\tAdress: \t" << locTable[ZooArea] << '\n';
}

Panda::Panda(const char* nm, int room, const char* s, const char* sci, ZooLocs loc) : Bear(s, loc, sci), indName(copyText(nm)), cell(room) {}

void Panda::isA() const {
    Bear::isA();
    std::cout << "\tCall our friend: \t" << indName << '\n';
}

void Panda::print() const {
    Bear::print();
    std::cout << "\tCell No: \t" << cell << '\n';
}

Tiger::Tiger(const char* nm, int enclosure, const char* s, const char* sci, ZooLocs loc) : ZooAnimal(s), sciName(copyText(sci)), indName(copyText(nm)), ZooArea(loc), enclosureNo(enclosure) {}

Tiger::~Tiger() {
    delete[] sciName;
    delete[] indName;
}

void Tiger::isA() const {
    ZooAnimal::isA();
    std::cout << "\tSname: \t" << sciName << '\n';
    std::cout << "\tCall our friend: \t" << indName << '\n';
}

void Tiger::print() const {
    ZooAnimal::print();
    std::cout << "\tAdress: \t" << locTable[ZooArea] << '\n';
    std::cout << "\tEnclosure No: \t" << enclosureNo << '\n';
}

Elephant::Elephant(const char* nm, int kg, const char* s, const char* sci, ZooLocs loc) : ZooAnimal(s), sciName(copyText(sci)), indName(copyText(nm)), ZooArea(loc), weight(kg) {}

Elephant::~Elephant() {
    delete[] sciName;
    delete[] indName;
}

void Elephant::isA() const {
    ZooAnimal::isA();
    std::cout << "\tSname: \t" << sciName << '\n';
    std::cout << "\tCall our friend: \t" << indName << '\n';
}

void Elephant::print() const {
    ZooAnimal::print();
    std::cout << "\tAdress: \t" << locTable[ZooArea] << '\n';
    std::cout << "\tWeight: \t" << weight << " kg\n";
}

void print(const ZooAnimal* pz) {
    while (pz) {
        pz->print();
        std::cout << '\n';
        pz = pz->next;
    }
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

bool readName(const std::string& prompt, std::string& value) {
    std::cout << prompt;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::size_t first = line.find_first_not_of(" \t");
        if (first != std::string::npos) {
            std::size_t last = line.find_last_not_of(" \t");
            std::string name = line.substr(first, last - first + 1);
            if (name.size() <= maxNameLength) {
                value = name;
                return true;
            }
        }
        std::cout << "Enter a name of 1 to " << maxNameLength << " characters: ";
    }
    return false;
}

ZooAnimal* readAnimal(int choice) {
    std::string name;
    int number;
    if (choice == 1) {
        if (!readName("Tiger's name: ", name) || !readInt("Enclosure No (1-999): ", 1, 999, number)) {
            return nullptr;
        }
        return new Tiger(name.c_str(), number);
    }
    if (!readName("Elephant's name: ", name) || !readInt("Weight in kg (100-10000): ", 100, 10000, number)) {
        return nullptr;
    }
    return new Elephant(name.c_str(), number);
}

int main() {
    ZooAnimal circus("Circus animal");
    Bear yogi("Little bear", BEAR, "ursus cartoonus");
    Panda yinYang("Yin Yang", 1001, "Big Panda");
    Panda rocky("Rocky", 943, "Red Panda", "Ailurus fulgena");
    Tiger raja("Raja", 12, "Bengal Tiger", "Panthera tigris tigris");
    Elephant tembo("Tembo", 5400);

    ZooAnimal* headPtr = &yinYang;
    headPtr->link(&circus);
    headPtr->link(&yogi);
    headPtr->link(&rocky);
    headPtr->link(&raja);
    headPtr->link(&tembo);

    std::cout << "Virtual Function Example\n";
    print(headPtr);

    ZooAnimal* added[maxAdded];
    int count = 0;
    int choice;
    bool ended = true;
    while (readInt("\nAdd (1 - tiger, 2 - elephant, 3 - show the zoo, 0 - exit): ", 0, 3, choice)) {
        if (choice == 0) {
            ended = false;
            break;
        }
        if (choice == 3) {
            std::cout << '\n';
            print(headPtr);
            continue;
        }
        if (count == maxAdded) {
            std::cout << "The zoo is full (" << maxAdded << " new animals)\n";
            continue;
        }
        ZooAnimal* animal = readAnimal(choice);
        if (!animal) {
            break;
        }
        added[count] = animal;
        ++count;
        headPtr->link(animal);
        std::cout << "Added:\n";
        animal->print();
    }
    std::cout << (ended ? "\nInput ended\n" : "Bye\n");

    for (int i = 0; i < count; ++i) {
        delete added[i];
    }
    return 0;
}

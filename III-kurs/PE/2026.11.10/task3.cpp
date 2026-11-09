#include <cstring>
#include <iostream>

enum ZooLocs { ZOOANIMAL, BEAR, PANDA };

const char* const locTable[] = {
    "Whole zoo area",
    "North B1: brown area",
    "East B1,P area"
};

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

void print(const ZooAnimal* pz) {
    while (pz) {
        pz->print();
        std::cout << '\n';
        pz = pz->next;
    }
}

ZooAnimal* makelist(Panda& yinYang, ZooAnimal& circus, Bear& yogi, Panda& rocky) {
    ZooAnimal* ptr = &yinYang;
    ptr->link(&circus);
    ptr->link(&yogi);
    ptr->link(&rocky);
    return ptr;
}

int main() {
    ZooAnimal circus("Circus animal");
    Bear yogi("Little bear", BEAR, "ursus cartoonus");
    Panda yinYang("Yin Yang", 1001, "Big Panda");
    Panda rocky("Rocky", 943, "Red Panda", "Ailurus fulgena");

    std::cout << "Virtual Function Example\n";
    ZooAnimal* headPtr = makelist(yinYang, circus, yogi, rocky);
    print(headPtr);
    return 0;
}

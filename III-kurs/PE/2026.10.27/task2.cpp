#include <cctype>
#include <iostream>
#include <limits>
#include <string>

const int MAX_STUDENTS = 10;

class Student {
private:
    std::string name;
    int facultyNumber;
    static int count;

public:
    Student() : name("Unknown"), facultyNumber(100000000) {
        ++count;
    }

    Student(const std::string& n, int fn) : name("Unknown"), facultyNumber(100000000) {
        ++count;
        set(n, fn);
    }

    Student(const Student& s) : name(s.name), facultyNumber(s.facultyNumber) {
        ++count;
    }

    ~Student() {
        --count;
    }

    static bool validFacultyNumber(int fn) {
        return fn >= 100000000 && fn <= 999999999;
    }

    bool set(const std::string& n, int fn) {
        if (n.empty() || !validFacultyNumber(fn)) return false;
        name = n;
        facultyNumber = fn;
        return true;
    }

    void show() const {
        std::cout << name << ' ' << facultyNumber << '\n';
    }

    static int getCount() {
        return count;
    }
};

int Student::count = 0;

std::string trim(const std::string& s) {
    std::string::size_type first = 0;
    std::string::size_type last = s.size();
    while (first < last && std::isspace(static_cast<unsigned char>(s[first]))) ++first;
    while (last > first && std::isspace(static_cast<unsigned char>(s[last - 1]))) --last;
    return s.substr(first, last - first);
}

bool readCount(int* n) {
    std::cout << "Enter N (1-10): ";
    while (!(std::cin >> *n) || *n < 1 || *n > MAX_STUDENTS) {
        if (std::cin.eof()) return false;
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }
        std::cout << "N must be a whole number from 1 to 10: ";
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    return true;
}

bool readName(std::string* name) {
    std::cout << "Name: ";
    std::string line;
    while (std::getline(std::cin, line)) {
        *name = trim(line);
        if (!name->empty()) return true;
        std::cout << "Name cannot be empty: ";
    }
    return false;
}

bool readFacultyNumber(int* fn) {
    std::cout << "Faculty number (9 digits): ";
    std::string line;
    while (std::getline(std::cin, line)) {
        std::string token = trim(line);
        bool digits = token.size() == 9 && token[0] != '0';
        for (char ch : token) {
            if (!std::isdigit(static_cast<unsigned char>(ch))) digits = false;
        }
        if (digits) {
            *fn = std::stoi(token);
            return true;
        }
        std::cout << "Faculty number must be exactly 9 digits: ";
    }
    return false;
}

int main() {
    int n;
    if (!readCount(&n)) {
        std::cout << "\nInput ended\n";
        return 0;
    }

    Student* students = new Student[n];
    for (int i = 0; i < n; ++i) {
        std::cout << "Student " << i + 1 << ":\n";
        std::string name;
        int fn;
        if (!readName(&name) || !readFacultyNumber(&fn)) {
            std::cout << "\nInput ended\n";
            delete[] students;
            return 0;
        }
        students[i].set(name, fn);
    }

    std::cout << '\n';
    for (int i = 0; i < n; ++i) students[i].show();

    std::cout << "Students: " << Student::getCount() << '\n';
    {
        Student extra("Extra Student", 121224999);
        std::cout << "Students in block: " << Student::getCount() << '\n';
    }
    std::cout << "Students after block: " << Student::getCount() << '\n';

    delete[] students;
    std::cout << "Students after delete[]: " << Student::getCount() << '\n';

    return 0;
}

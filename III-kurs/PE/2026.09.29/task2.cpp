#include <iostream>
#include <string>

const int MAX_SALARIES = 12;

class Worker {
private:
    long long ssn;
    std::string name;
    int yearsOfService;
    std::string position;
    double salaries[MAX_SALARIES];
    int salaryCount;

public:
    Worker() : ssn(0), name(""), yearsOfService(0), position(""), salaryCount(0) {}

    Worker(const std::string& workerName) : ssn(0), name(workerName), yearsOfService(0), salaryCount(0) {
        std::cout << "Enter current position for " << name << ": ";
        std::getline(std::cin, position);
    }

    void setSsn(long long value) { ssn = value; }
    void setName(const std::string& value) { name = value; }
    void setPosition(const std::string& value) { position = value; }

    bool setYearsOfService(int value) {
        if (value < 0) return false;
        yearsOfService = value;
        return true;
    }

    bool addSalary(double value) {
        if (value < 0 || salaryCount >= MAX_SALARIES) return false;
        salaries[salaryCount++] = value;
        return true;
    }

    long long getSsn() const { return ssn; }
    std::string getName() const { return name; }
    int getYearsOfService() const { return yearsOfService; }
    std::string getPosition() const { return position; }
    int getSalaryCount() const { return salaryCount; }

    double getSalary(int index) const {
        if (index < 0 || index >= salaryCount) return 0;
        return salaries[index];
    }

    double averageSalary() const {
        if (salaryCount == 0) return 0;
        double sum = 0;
        for (int i = 0; i < salaryCount; i++) sum += salaries[i];
        return sum / salaryCount;
    }

    double minSalary() const {
        if (salaryCount == 0) return 0;
        double min = salaries[0];
        for (int i = 1; i < salaryCount; i++)
            if (salaries[i] < min) min = salaries[i];
        return min;
    }

    void print() const {
        std::cout << "SSN: " << ssn << '\n'
                  << "Name: " << name << '\n'
                  << "Years of service: " << yearsOfService << '\n'
                  << "Position: " << position << '\n'
                  << "Salaries:";
        for (int i = 0; i < salaryCount; i++) std::cout << ' ' << salaries[i];
        std::cout << "\nAverage salary: " << averageSalary() << '\n'
                  << "Minimum salary: " << minSalary() << "\n\n";
    }
};

int main() {
    Worker first;
    first.setSsn(9001011234LL);
    first.setName("Ivan Petrov");
    first.setYearsOfService(5);
    first.setPosition("Engineer");
    first.addSalary(2500);
    first.addSalary(2700);
    first.addSalary(2400);
    std::cout << "Worker created with the default constructor:\n";
    first.print();

    Worker second("Maria Ivanova");
    second.setSsn(9505059876LL);
    second.setYearsOfService(2);
    second.addSalary(1800);
    second.addSalary(1950);
    second.addSalary(1700);
    second.addSalary(2100);
    std::cout << "\nWorker created with the position read from the keyboard:\n";
    second.print();

    return 0;
}

#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <chrono>
using namespace std;

const int START_BALANCE = 1000;
const int SUM = 10;
const int OPERATIONS = 1000;

class Account {
    int balance;
    mutex m;
    bool useMutex;

    void change(int delta) {
        int tmp = balance;
        this_thread::sleep_for(1us);   // прави състезанието видимо
        balance = tmp + delta;
    }

public:
    Account(int balance, bool useMutex) : balance(balance), useMutex(useMutex) {}

    void deposit(int sum) {
        if (useMutex) {
            lock_guard<mutex> lock(m);
            change(sum);
        } else {
            change(sum);
        }
    }

    bool withdraw(int sum) {
        if (useMutex) {
            lock_guard<mutex> lock(m);
            if (balance < sum) {
                return false;
            }
            change(-sum);
            return true;
        }
        if (balance < sum) {
            return false;
        }
        change(-sum);
        return true;
    }

    int getBalance() {
        lock_guard<mutex> lock(m);
        return balance;
    }
};

void client(Account &account) {
    for (int i = 0; i < OPERATIONS; i++) {
        account.deposit(SUM);
    }
    for (int i = 0; i < OPERATIONS; i++) {
        account.withdraw(SUM);
    }
}

void run(const char *name, bool useMutex) {
    Account account(START_BALANCE, useMutex);
    vector<thread> threads;
    for (int i = 0; i < 3; i++) {
        threads.emplace_back(client, ref(account));
    }
    for (thread &t : threads) {
        t.join();
    }
    cout << name << account.getBalance() << " лв. (expected " << START_BALANCE << " лв.)" << endl;
}

int main() {
    for (int i = 1; i <= 3; i++) {
        run("С mutex:   ", true);
    }
    for (int i = 1; i <= 3; i++) {
        run("Без mutex: ", false);
    }
}

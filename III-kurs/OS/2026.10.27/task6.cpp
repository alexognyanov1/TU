#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>
using namespace std;

int counter = 0;
mutex m;

void incrementUnsafe() {
    for (int i = 0; i < 100; i++) {
        int tmp = counter;
        this_thread::sleep_for(1ms);
        counter = tmp + 1;
    }
}

void incrementSafe() {
    for (int i = 0; i < 100; i++) {
        lock_guard<mutex> lock(m);     // отключва се в края на итерацията
        int tmp = counter;
        this_thread::sleep_for(1ms);
        counter = tmp + 1;
    }
}

void run(const char *name, void (*f)()) {
    counter = 0;
    auto start = chrono::steady_clock::now();
    thread a(f), b(f);
    a.join();
    b.join();
    auto ms = chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now() - start).count();
    cout << name << counter << " (expected 200), " << ms << " ms" << endl;
}

int main() {
    run("Без mutex:  ", incrementUnsafe);
    run("С mutex:    ", incrementSafe);
}

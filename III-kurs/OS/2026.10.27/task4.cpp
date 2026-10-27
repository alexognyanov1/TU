#include <iostream>
#include <thread>
#include <chrono>
using namespace std;

void tik() {
    for (int i = 0; i < 5; i++) {
        cout << "тик" << endl;
        this_thread::sleep_for(500ms);
    }
}

void tak() {
    for (int i = 0; i < 5; i++) {
        cout << "    так" << endl;
        this_thread::sleep_for(800ms);
    }
}

int main() {
    auto start = chrono::steady_clock::now();

    thread a(tik), b(tak);
    a.join();
    b.join();

    auto end = chrono::steady_clock::now();
    auto ms = chrono::duration_cast<chrono::milliseconds>(end - start).count();
    cout << "Общо време: " << ms << " ms (тик: 2500 ms, так: 4000 ms, сбор: 6500 ms)" << endl;
}

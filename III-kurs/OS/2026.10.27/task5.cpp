#include <iostream>
#include <thread>
#include <chrono>
#include <vector>
using namespace std;

int counter = 0;

void incrementSlow() {
    for (int i = 0; i < 100; i++) {
        int tmp = counter;             // 1. чете
        this_thread::sleep_for(1ms);   // 2. "работи"
        counter = tmp + 1;             // 3. записва
    }
}

void incrementFast() {
    for (int i = 0; i < 1000000; i++) {
        counter++;
    }
}

int main() {
    counter = 0;
    thread a(incrementSlow), b(incrementSlow);
    a.join();
    b.join();
    cout << "Със заспиване, 2 нишки x 100:       " << counter << " (expected 200)" << endl;

    counter = 0;
    vector<thread> threads;
    for (int i = 0; i < 4; i++) {
        threads.emplace_back(incrementFast);
    }
    for (thread &t : threads) {
        t.join();
    }
    cout << "Без заспиване, 4 нишки x 1 000 000: " << counter << " (expected 4000000)" << endl;
}

#include <iostream>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>
#include <chrono>
using namespace std;

const int THREADS = 4;
const int ITERATIONS = 1000000;

int counterMutex = 0;
mutex m;
atomic<int> counterAtomic(0);

void incrementMutex() {
    for (int i = 0; i < ITERATIONS; i++) {
        lock_guard<mutex> lock(m);
        counterMutex++;
    }
}

void incrementAtomic() {
    for (int i = 0; i < ITERATIONS; i++) {
        counterAtomic++;
    }
}

long long measure(void (*f)()) {
    auto start = chrono::steady_clock::now();
    vector<thread> threads;
    for (int i = 0; i < THREADS; i++) {
        threads.emplace_back(f);
    }
    for (thread &t : threads) {
        t.join();
    }
    return chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now() - start).count();
}

int main() {
    long long msMutex = measure(incrementMutex);
    cout << "mutex:       " << counterMutex << " (expected 4000000), " << msMutex << " ms" << endl;

    long long msAtomic = measure(incrementAtomic);
    cout << "atomic<int>: " << counterAtomic << " (expected 4000000), " << msAtomic << " ms" << endl;
}

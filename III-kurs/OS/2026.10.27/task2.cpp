#include <iostream>
#include <thread>
#include <vector>
using namespace std;

void worker(int id) {
    cout << "Нишка " << id << endl;
}

int main() {
    vector<thread> threads;
    for (int i = 1; i <= 5; i++)
        threads.emplace_back(worker, i);

    for (thread &t : threads)
        t.join();
}

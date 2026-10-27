#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>
using namespace std;

mutex m1, m2;

void threadA() {
    lock_guard<mutex> l1(m1);
    cout << "A took m1" << endl;
    this_thread::sleep_for(100ms);     // време за B да вземе m2
    lock_guard<mutex> l2(m2);          // чака B завинаги
    cout << "A took both" << endl;
}

void threadB() {
    lock_guard<mutex> l2(m2);
    cout << "B took m2" << endl;
    this_thread::sleep_for(100ms);     // време за A да вземе m1
    lock_guard<mutex> l1(m1);          // чака A завинаги
    cout << "B took both" << endl;
}

int main() {
    thread a(threadA), b(threadB);
    a.join();
    b.join();
    cout << "This message is not going to be shown" << endl;
}

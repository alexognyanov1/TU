#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>
using namespace std;

mutex m1, m2;

// (а) еднакъв ред на заключване: и двете нишки първо m1, после m2
void orderedA() {
    lock_guard<mutex> l1(m1);
    this_thread::sleep_for(100ms);
    lock_guard<mutex> l2(m2);
    cout << "(а) A took both" << endl;
}

void orderedB() {
    lock_guard<mutex> l1(m1);
    this_thread::sleep_for(100ms);
    lock_guard<mutex> l2(m2);
    cout << "(а) B took both" << endl;
}

// (б) scoped_lock заключва двата мютекса наведнъж, редът няма значение
void scopedA() {
    scoped_lock lock(m1, m2);
    this_thread::sleep_for(100ms);
    cout << "(б) A took both" << endl;
}

void scopedB() {
    scoped_lock lock(m2, m1);
    this_thread::sleep_for(100ms);
    cout << "(б) B took both" << endl;
}

int main() {
    thread a(orderedA), b(orderedB);
    a.join();
    b.join();
    cout << "(а) еднакъв ред: програмата продължава" << endl;

    thread c(scopedA), d(scopedB);
    c.join();
    d.join();
    cout << "(б) scoped_lock: програмата завършва" << endl;
}

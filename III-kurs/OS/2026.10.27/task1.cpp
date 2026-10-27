#include <iostream>
#include <thread>
using namespace std;

void hello() {
    cout << "Здравей от нишка!" << endl;
}

int main() {
    thread t(hello);
    t.join();
    cout << "Край" << endl;
}

#include <iostream>
#include <thread>
using namespace std;

void sum(long long n, long long &result) {
    result = 0;
    for (long long i = 1; i <= n; i++)
        result += i;
}

int main() {
    long long n = 100;
    long long result = 0;
    thread t(sum, n, ref(result));
    t.join();
    cout << "Сборът от 1 до " << n << " е " << result << endl;
}

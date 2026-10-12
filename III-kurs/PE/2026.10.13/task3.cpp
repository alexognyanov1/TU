#include <cstdlib>
#include <iostream>
#include <limits>

const int STACK_SIZE = 26;

class Stack {
private:
    char data[STACK_SIZE];
    int top;

public:
    Stack() : top(0) {}

    bool push(char ch) {
        if (top == STACK_SIZE) return false;
        data[top++] = ch;
        return true;
    }

    bool pop(char* ch) {
        if (top == 0) return false;
        *ch = data[--top];
        return true;
    }

    bool isEmpty() const { return top == 0; }
    int size() const { return top; }
};

Stack loadstack() {
    Stack s;
    for (char ch = 'a'; ch <= 'z'; ++ch) s.push(ch);
    return s;
}

Stack loadstack(int upper) {
    Stack s;
    char first = upper == 1 ? 'A' : 'a';
    for (int i = 0; i < STACK_SIZE; ++i) s.push(static_cast<char>(first + i));
    return s;
}

void showstack(const char* title, Stack s) {
    std::cout << title << " (" << s.size() << " symbols): ";
    char ch;
    while (!s.isEmpty()) {
        s.pop(&ch);
        std::cout << ch;
    }
    std::cout << '\n';
}

int main() {
    showstack("loadstack()", loadstack());
    showstack("loadstack(1)", loadstack(1));
    showstack("loadstack(0)", loadstack(0));

    int upper;
    std::cout << "Enter upper (1 = capital letters, anything else = small letters): ";
    while (!(std::cin >> upper)) {
        if (std::cin.eof()) {
            std::cout << "\nInput ended\n";
            return 0;
        }
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Please enter a whole number: ";
    }
    std::cout << '\n';

    Stack s = loadstack(upper);
    showstack("loadstack(upper)", s);

    Stack* ps = &s;
    char ch;
    if (ps->pop(&ch)) std::cout << "Popped through a pointer: " << ch << ", left " << ps->size() << '\n';
    std::cout << "Push on a full stack: " << (loadstack().push('#') ? "accepted" : "rejected") << '\n';
    Stack empty;
    std::cout << "Pop from an empty stack: " << (empty.pop(&ch) ? "succeeded" : "rejected") << '\n';

    return 0;
}

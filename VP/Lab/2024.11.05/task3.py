# Description: This script modifies a list of numbers by setting elements greater than a threshold to zero.
# Tags: List Modification, Threshold

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Деление на нула не е позволено!")
    return a / b


permitted_operations = ['+', '-', '*', '/']


def calculator():
    print("Изберете операция:")
    print("+ Събиране")
    print("- Изваждане")
    print("* Умножение")
    print("/ Деление")

    operation = input("Операция: ")
    while operation not in permitted_operations:
        print("Невалидна операция!")
        operation = input("Операция: ")
    num1 = int(input("Първо число: "))
    num2 = int(input("Второ число: "))

    result = None
    if operation == '+':
        result = add(num1, num2)
    elif operation == '-':
        result = subtract(num1, num2)
    elif operation == '*':
        result = multiply(num1, num2)
    elif operation == '/':
        try:
            result = divide(num1, num2)
        except ValueError as e:
            print(e)
            return
    else:
        print("Невалидна операция!")
        return

    print(f"Резултат: {result}")


if __name__ == "__main__":
    calculator()

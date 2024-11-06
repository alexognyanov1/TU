# Description: This script performs various tasks based on user input, including unit conversion, greeting, and financial calculations.
# Tags: Lab, Python, User Input, Unit Conversion, Financial Calculations

def task_1():
    inch = float(input())

    print("cm: " + str(inch * 2.54))


def task_2():
    name = input()

    print("Hello, " + name + "!")


def task_3():
    first_name = input("First name:")
    last_name = input("Last name:")
    age = int(input("Age:"))
    city = input("City:")

    print(
        f"You are {first_name} {last_name}, a {age}-years old person from {city}.")


def task_4():
    packages_dog = int(input())
    while packages_dog < 0 or packages_dog > 25:
        print("Invalid input!")
        packages_dog = int(input())

    packages_cat = int(input())
    while packages_cat < 0 or packages_cat > 25:
        print("Invalid input!")
        packages_cat = int(input())

    print(f"{packages_dog * 2.5 + packages_cat * 4:.2f} lv.")


def task_5():
    price_vegetables = float(input())
    price_fruits = float(input())
    weight_vegetables = int(input())
    weight_fruits = int(input())

    print(f"{(price_vegetables * weight_vegetables + price_fruits * weight_fruits) / 1.94:.2f} EUR")


def task_6():
    dollar = float(input())

    while dollar < 100 or dollar > 5000:
        print("Invalid input!")
        dollar = float(input())

    lira = float(input())

    while lira < 100 or lira > 5000:
        print("Invalid input!")
        lira = float(input())

    commission = float(input())

    while commission < 1 or commission > 6:
        print("Invalid input!")
        commission = float(input())

    print(f"{(dollar * 1.76 + lira * 0.052) / 1.96 * (1 - commission / 100):.2f}")


task_6()

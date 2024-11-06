# Description: This script generates a random list and inserts sums between elements.
# Tags: Random List, List Modification

import random


def generate_random_list(size, min_value, max_value):
    return [random.randint(min_value, max_value) for _ in range(size)]


def insert_sums_between_elements(numbers):
    result = []

    for i in range(len(numbers) - 1):
        result.append(numbers[i])

        result.append(numbers[i] + numbers[i + 1])

    result.append(numbers[-1])

    return result


def main():
    try:
        size = int(input("Въведете размера на списъка: "))
        min_value = int(input("Въведете минималната стойност: "))
        max_value = int(input("Въведете максималната стойност: "))

        if size < 2:
            print("Списъкът трябва да има поне 2 елемента.")
            return

        random_list = generate_random_list(size, min_value, max_value)
        print("Начален списък:", random_list)

        modified_list = insert_sums_between_elements(random_list)
        print("Модифициран списък със суми между елементите:", modified_list)

    except ValueError:
        print("Моля, въведете валидни цели числа.")


if __name__ == "__main__":
    main()

import random


def get_user_input():
    try:
        n = int(input("Въведете цяло число между 20 и 30: "))
        if not (20 < n < 30):
            raise ValueError("Числото трябва да бъде между 20 и 30.")

        return n
    except ValueError as e:
        print(f"Невалидна стойност: {e}")
        return


def generate_array(n):
    arr = []
    for i in range(n):
        arr.append(random.randint(-99, 99))

    return arr


def find_sum_of_odd_indices(arr):
    sum = 0
    for i in range(1, len(arr)):
        if i % 2 != 0:
            sum += arr[i]

    return sum


def find_count_of_units_multiple_of_2(arr):
    count = 0
    for num in arr:
        if abs(num) % 10 % 2 == 0:
            count += 1

    return count


def find_product_of_negative_even(arr):
    product = 1
    has_negative_even = False
    for num in arr:
        if num < 0 and num % 2 == 0:
            product *= num
            has_negative_even = True

    if not has_negative_even:
        product = 0

    return product


def filter_bigger_than_n(arr, n):
    new_arr = []

    for num in arr:
        if num > n:
            new_arr.append(num)

    return new_arr


def find_diff_min_max(arr):
    if not arr:
        return 0

    return max(arr) - min(arr)


def print_odd_numbers(arr):
    odd_numbers = []

    for num in arr:
        if num % 2 != 0:
            odd_numbers.append(num)

    print(odd_numbers, len(odd_numbers))


def delete_min_element(arr):
    if not arr:
        return []

    min_value = min(arr)
    arr.remove(min_value)

    return arr


def main():
    n = get_user_input()

    arr1 = generate_array(n)
    odd_indices_sum = find_sum_of_odd_indices(arr1)
    multiple_of_2_count = find_count_of_units_multiple_of_2(arr1)
    negative_even_product = find_product_of_negative_even(arr1)

    arr2 = filter_bigger_than_n(arr1, n)
    diff_min_max = find_diff_min_max(arr2)
    print_odd_numbers(arr2)
    arr2 = delete_min_element(arr2)


if __name__ == "__main__":
    main()

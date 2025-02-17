# Description: This script creates a list of integers based on user input, performs various operations on the list such as counting elements based on specific criteria, finding indices of minimum elements, creating a second list based on conditions, calculating averages, removing elements, and adding a new element based on existing odd numbers.  The script then prints the results of each operation.
# Tags: List Manipulation, Integer Processing, Data Filtering, List Modification

def get_list_length():
    while True:
        try:
            n = int(input("Enter the number of elements (between 15 and 35): "))
            if 15 < n < 35:
                return n
            else:
                print("Number must be between 15 and 35.")
        except ValueError:
            print("Invalid input. Please enter an integer.")


def create_list(n):
    lst = []
    for _ in range(n):
        while True:
            try:
                num = int(input("Enter a positive integer between 30 and 300: "))
                if 30 <= num <= 300:
                    lst.append(num)
                    break
                else:
                    print("Number must be between 30 and 300.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
    return lst


def count_elements_with_tens_digit_multiple_of_3(lst):
    count = 0
    for x in lst:
        if (x // 10) % 3 == 0:
            count += 1
    return count


def find_index_of_min_element_with_remainder_4(lst):
    min_element = float('inf')
    min_index = -1
    for i, num in enumerate(lst):
        if num % 6 == 4 and num < min_element:
            min_element = num
            min_index = i
    return min_index


def create_second_list(lst):
    second_list = []
    for x in lst:
        if 10 <= x < 100 and (x % 2 == 0 or x % 3 == 0):
            second_list.append(x)
    return second_list


def calculate_average_of_odd_indices(lst):
    odd_index_elements = []
    for i in range(1, len(lst), 2):
        odd_index_elements.append(lst[i])
    if odd_index_elements:
        return sum(odd_index_elements) / len(odd_index_elements)
    else:
        return 0


def remove_min_even_element(lst):
    min_even = float('inf')
    min_index = -1
    for i, num in enumerate(lst):
        if num % 2 == 0 and num < min_even:
            min_even = num
            min_index = i
    if min_index != -1:
        lst.pop(min_index)


def add_new_element(lst):
    odd_numbers = []
    for x in lst:
        if x % 2 != 0:
            odd_numbers.append(x)
    if odd_numbers:
        new_element = max(odd_numbers) * min(odd_numbers)
        lst.insert(0, new_element)


def main():
    n = get_list_length()
    lst = create_list(n)

    print("List created:", lst)
    print("Count of elements with tens digit multiple of 3:",
          count_elements_with_tens_digit_multiple_of_3(lst))
    print("Index of minimum element with remainder 4 when divided by 6:",
          find_index_of_min_element_with_remainder_4(lst))

    second_list = create_second_list(lst)
    print("Second list:", second_list)

    print("Average of elements at odd indices:",
          calculate_average_of_odd_indices(lst))

    remove_min_even_element(lst)
    print("List after removing minimum even element:", lst)

    add_new_element(lst)
    print("List after adding new element:", lst)


if __name__ == "__main__":
    main()
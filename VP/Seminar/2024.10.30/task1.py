# Description: This script calculates the multiplication of all numbers in a range that are divisible by 3 or 4.
# Tags: Multiplication, Range

def find_multiplication(m, n):
    result = 1
    for i in range(m, n + 1):
        if i % 3 == 0 or i % 4 == 0:
            result *= i
    return result


def main():
    m = int(input("Enter the starting number (m): "))
    n = int(input("Enter the ending number (n): "))
    if m > n:
        print("Invalid input: m should be less than or equal to n.")
        return
    multiplication_result = find_multiplication(m, n)
    print(
        f"The multiplication of all numbers from {m} to {n} that are divisible by 3 or 4 is: {multiplication_result}")


if __name__ == "__main__":
    main()

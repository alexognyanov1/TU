# Description: This script checks if a given number is a palindrome.
# Tags: Palindrome

def is_palindrome(number):
    num_str = str(number)
    return 1 if num_str == num_str[::-1] else 0


if __name__ == "__main__":
    while True:
        num = input("Enter a number: ")
        if num == 'exit':
            break

        if num.isdigit():
            print(
                f"Number {num} is{' ' if is_palindrome(num) else ' not '}a palindrome")
        else:
            print("Invalid input. Please enter a number")

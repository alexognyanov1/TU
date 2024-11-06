# Description: This script calculates the sum of prime and non-prime numbers entered by the user.
# Tags: Prime Numbers

def is_prime(n):
    if n <= 1:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True


def main():
    prime_sum = 0
    non_prime_sum = 0

    while True:
        user_input = input("Enter an integer (or 'stop' to finish): ")

        if user_input.lower() == 'stop':
            break

        try:
            number = int(user_input)

            if number < 0:
                print("Number is negative.")
                continue

            if is_prime(number):
                prime_sum += number
            else:
                non_prime_sum += number

        except ValueError:
            print("Invalid input. Please enter an integer or 'stop' to finish.")

    print(f"Sum of prime numbers: {prime_sum}")
    print(f"Sum of non-prime numbers: {non_prime_sum}")


if __name__ == "__main__":
    main()

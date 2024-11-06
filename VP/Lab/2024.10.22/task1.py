# Description: This script validates user input, forms tuples of digits in normal and reverse order.
# Tags: Lab, Python, User Input, Tuples

def validate_input():
    while True:
        try:
            number = input("Моля, въведете цяло число: ")

            number = int(number)

            return number

        except ValueError:
            print("Невалидно число. Моля, опитайте отново.")


def form_tuples(number):
    digits = tuple(str(number))
    reverse_digits = tuple(str(number)[::-1])

    return digits, reverse_digits


def main():
    try:
        number = validate_input()

        digits, reverse_digits = form_tuples(number)

        print("Кортеж с цифрите в прав ред:", digits)
        print("Кортеж с цифрите в обратен ред:", reverse_digits)

    except OverflowError:
        print("Въведеното число е твърде голямо за обработка.")
    except Exception as e:
        print(f"Възникна неочаквана грешка: {e}")


if __name__ == "__main__":
    main()

# Description: This script validates user input and creates a dictionary with character counts.
# Tags: Character Count

def validate_input():
    while True:
        text = input("Моля, въведете текст: ")

        if len(text.strip()) == 0:
            print("Текстът не може да бъде празен. Опитайте отново.")
        else:
            return text


def create_char_count_dict(text):
    char_count = {}

    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    return char_count


def main():
    text = validate_input()

    char_count_dict = create_char_count_dict(text)

    print("Речник с броя на символите в текста:")
    for char, count in char_count_dict.items():
        print(f"'{char}': {count}")


if __name__ == "__main__":
    main()

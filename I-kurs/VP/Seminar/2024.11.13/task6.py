# Description: This script implements a simple English-Bulgarian dictionary program. It allows users to search for words, add new words, view the dictionary, delete words, and exit the program.
# Tags: Dictionary, Language Learning, User Interface, Data Management 

def display_menu():
    print("English-Bulgarian Dictionary")
    print("1. Search for a word")
    print("2. Add a word")
    print("3. View dictionary")
    print("4. Delete a word")
    print("5. Exit")


def search_word(dictionary):
    word = input("Enter the English word to search: ").strip()
    if word in dictionary:
        print(f"The Bulgarian translation is: {dictionary[word]}")
    else:
        print("Word not found in the dictionary.")
        add = input(
            "Would you like to add this word to the dictionary? (yes/no): ").strip().lower()
        if add == 'yes':
            translation = input("Enter the Bulgarian translation: ").strip()
            dictionary[word] = translation
            print("Word added to the dictionary.")


def add_word(dictionary):
    word = input("Enter the English word to add: ").strip()
    if word in dictionary:
        print("Word already exists in the dictionary.")
    else:
        translation = input("Enter the Bulgarian translation: ").strip()
        dictionary[word] = translation
        print("Word added to the dictionary.")


def view_dictionary(dictionary):
    if dictionary:
        for word, translation in dictionary.items():
            print(f"{word}: {translation}")
    else:
        print("The dictionary is empty.")


def delete_word(dictionary):
    word = input("Enter the English word to delete: ").strip()
    if word in dictionary:
        del dictionary[word]
        print("Word deleted from the dictionary.")
    else:
        print("Word not found in the dictionary.")


def main():
    dictionary = {}
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            search_word(dictionary)
        elif choice == '2':
            add_word(dictionary)
        elif choice == '3':
            view_dictionary(dictionary)
        elif choice == '4':
            delete_word(dictionary)
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
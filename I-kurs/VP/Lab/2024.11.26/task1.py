# Description: This script simulates a library system. It allows users to add books, search for books by title or author, borrow books, return books, and view available and borrowed books.  The system tracks book availability and the number of times each book has been borrowed. It also limits the number of books a user can borrow simultaneously.
# Tags: Library Management, Book Tracking, Inventory Management

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.is_available = True
        self.borrow_count = 0

    def print_info(self):
        print(
            f"Заглавие: {self.title}, Автор: {self.author}, Година: {self.year}")

    def borrow(self):
        if self.is_available:
            self.is_available = False
            self.borrow_count += 1
            print(f"Вие наехте книгата {self.title}")
        else:
            print(f"Книгата {self.title} вече е заета.")

    def return_book(self):
        self.is_available = True
        print(f"Вие върнахте книгата {self.title}")


class Library:
    def __init__(self):
        self.books = []
        self.borrowed_books = {}

    def add_book(self, book):
        self.books.append(book)

    def print_available_books(self):
        for book in self.books:
            if book.is_available:
                print(book.title)

    def borrow_book(self, title, user):
        if user not in self.borrowed_books:
            self.borrowed_books[user] = []

        if len(self.borrowed_books[user]) >= 3:
            print("Не можете да наемете повече от 3 книги наведнъж.")
            return

        for book in self.books:
            if book.title == title:
                if book.is_available:
                    book.borrow()
                    self.borrowed_books[user].append(book)
                else:
                    print(f"Книгата {title} вече е заета.")
                return
        print(f"Книгата {title} не е намерена.")

    def return_book(self, title, user):
        if user in self.borrowed_books:
            for book in self.borrowed_books[user]:
                if book.title == title:
                    book.return_book()
                    self.borrowed_books[user].remove(book)
                    return
        print(f"Книгата {title} не е намерена или не е наета от {user}.")

    def print_borrowed_books(self):
        for user, books in self.borrowed_books.items():
            for book in books:
                print(f"Читател: {user}, Книга: {book.title}")

    def search_books(self, query):
        found_books = [book for book in self.books if query.lower(
        ) in book.title.lower() or query.lower() in book.author.lower()]
        if found_books:
            for book in found_books:
                book.print_info()
        else:
            print("Няма намерени книги по зададения критерий.")


if __name__ == "__main__":
    library = Library()

    book1 = Book("Под игото", "Иван Вазов", 1894)
    book2 = Book("Тютюн", "Димитър Димов", 1951)
    book3 = Book("Железният светилник", "Димитър Талев", 1952)

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    print("Налични книги в библиотеката:")
    library.print_available_books()

    print("\nТърсене на книги по автор 'Димитър':")
    library.search_books("Димитър")

    print("\nНаемане на книга 'Тютюн' от потребител 'Алекс':")
    library.borrow_book("Тютюн", "Алекс")

    print("\nНалични книги в библиотеката след наемане:")
    library.print_available_books()

    print("\nВърнати книги от потребител 'Алекс':")
    library.return_book("Тютюн", "Алекс")

    print("\nНалични книги в библиотеката след връщане:")
    library.print_available_books()

    print("\nНаемане на повече от 3 книги от потребител 'Алекс':")
    library.borrow_book("Под игото", "Алекс")
    library.borrow_book("Тютюн", "Алекс")
    library.borrow_book("Железният светилник", "Алекс")
    library.borrow_book("Под игото", "Алекс")
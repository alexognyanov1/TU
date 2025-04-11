#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MIN_CAPACITY 10

typedef struct {
  char title[30];
  char author[30];
  int year;
  double price;
} Book;

Book scanBook() {
  char title[30];
  char author[30];
  int year;
  double price;

  printf("Title: ");
  fgets(title, 29, stdin);
  size_t lenTitle = strlen(title);
  if (lenTitle > 0 && title[lenTitle - 1] == '\n') {
    title[lenTitle - 1] = '\0';
  }

  printf("Author: ");
  fgets(author, 29, stdin);
  size_t lenAuthor = strlen(author);
  if (lenAuthor > 0 && author[lenAuthor - 1] == '\n') {
    author[lenAuthor - 1] = '\0';
  }

  printf("Year: ");
  scanf("%d%*c", &year);

  printf("Price: ");
  scanf("%lf%*c", &price);

  Book b;
  strcpy(b.title, title);
  strcpy(b.author, author);
  b.year = year;
  b.price = price;

  return b;
}

void appendBook(Book *books, int *len, int *capacity, Book b) {
  if (*len >= *capacity) {
    *capacity *= 2;
    books = realloc(books, *capacity);
  }

  books[*len] = b;
  *len += 1;
}

void printBook(Book b) {
  printf("Title: %s\n", b.title);
  printf("Author: %s\n", b.author);
  printf("Year: %d\n", b.year);
  printf("Price: %.2f\n", b.price);
}

void stats(Book *books, int len) {
  double minPrice = books[0].price;
  double maxPrice = books[0].price;
  int indexCheapest = 0;
  int indexMostExpensive = 0;
  double sum = 0;

  for (int i = 1; i < len; i++) {
    sum += books[i].price;

    if (books[i].price < minPrice) {
      minPrice = books[i].price;
      indexCheapest = i;
    }

    if (books[i].price > maxPrice) {
      maxPrice = books[i].price;
      indexMostExpensive = i;
    }
  }

  printf("Cheapest: \n");
  printBook(books[indexCheapest]);
  printf("Most Expensive: \n");
  printBook(books[indexMostExpensive]);
  printf("Avg Price: %lf\n", sum / len);
}

int main() {
  int capacity = MIN_CAPACITY;
  int len = 0;
  Book *books = malloc(sizeof(Book) * capacity);

  for (int i = 0; i < 3; i++) {
    Book b = scanBook();
    appendBook(books, &len, &capacity, b);
  }

  stats(books, len);

  free(books);
}
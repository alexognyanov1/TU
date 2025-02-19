#include <stdio.h>

void printDigits();
void printLowercaseLetters();
void printUppercaseLetters();

int main() {
  char input;
  printf("Enter character: ");
  scanf("%c", &input);
  printf("%d\n", input);
  printDigits();
  printLowercaseLetters();
  printUppercaseLetters();
  return 0;
}

void printDigits() {
  printf("Digits from ASCII table:\n");
  for (char c = '0'; c <= '9'; c++) {
    printf("%c ", c);
  }
  printf("\n");
}

void printLowercaseLetters() {
  printf("Lowercase letters from ASCII table:\n");
  for (char c = 'a'; c <= 'z'; c++) {
    printf("%c ", c);
  }
  printf("\n");
}

void printUppercaseLetters() {
  printf("Uppercase letters from ASCII table:\n");
  for (char c = 'A'; c <= 'Z'; c++) {
    printf("%c ", c);
  }
  printf("\n");
}
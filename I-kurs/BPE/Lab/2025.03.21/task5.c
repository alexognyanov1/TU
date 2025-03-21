#include <ctype.h>
#include <stdio.h>

int countVowels(const char *str) {
  int count = 0;
  while (*str) {
    char ch = tolower(*str);
    if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
      count++;
    }
    str++;
  }
  return count;
}

int main() {
  char str[] = "asdfaa";
  printf("Number of vowels: %d\n", countVowels(str));
  return 0;
}
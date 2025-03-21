#include <stdio.h>

#define ALPHABET_SIZE 26

void countLetters(const char *str, int *counts) {
  while (*str) {
    if ((*str >= 'a' && *str <= 'z') || (*str >= 'A' && *str <= 'Z')) {
      if (*str >= 'A' && *str <= 'Z') {
        counts[*str - 'A']++;
      } else {
        counts[*str - 'a']++;
      }
    }
    str++;
  }
}

void printLetterCounts(const int *counts) {
  for (int i = 0; i < ALPHABET_SIZE; i++) {
    if (counts[i] > 0) {
      printf("%c: %d\n", 'a' + i, counts[i]);
    }
  }
}

int main() {
  char str[100];
  int counts[ALPHABET_SIZE] = {0};

  printf("Enter a string: ");
  fgets(str, sizeof(str), stdin);

  countLetters(str, counts);
  printLetterCounts(counts);

  return 0;
}
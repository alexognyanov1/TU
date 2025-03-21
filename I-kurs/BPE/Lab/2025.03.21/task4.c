#include <stdio.h>

int compareStrings(const char *str1, const char *str2) {
  while (*str1 && (*str1 == *str2)) {
    str1++;
    str2++;
  }
  return (unsigned char)*str1 - (unsigned char)*str2;
}

int main() {
  char str1[100], str2[100];

  printf("Enter first string: ");
  fgets(str1, sizeof(str1), stdin);

  printf("Enter second string: ");
  fgets(str2, sizeof(str2), stdin);

  int result = compareStrings(str1, str2);

  if (result < 0) {
    printf("First string is less than second string.\n");
  } else if (result > 0) {
    printf("First string is greater than second string.\n");
  } else {
    printf("Both strings are equal.\n");
  }

  return 0;
}
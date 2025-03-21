#include <ctype.h>
#include <stdio.h>

void to_uppercase(char *str) {
  while (*str) {
    *str = toupper((unsigned char)*str);
    str++;
  }
}

int main() {
  char str[100];

  printf("Enter a string: ");
  fgets(str, sizeof(str), stdin);

  to_uppercase(str);

  printf("Uppercase string: %s\n", str);

  return 0;
}
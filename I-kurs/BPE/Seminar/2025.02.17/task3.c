#include <stdio.h>

int main() {
  char ch;
  printf("Enter a character: ");
  scanf("%c", &ch);

  for (int i = 0; i < 5; i++) {
    for (int j = 0; j < 10; j++) {
      if (i == 0 || i == 4 || j == 0 || j == 9) {
        printf("%c", ch);
      } else {
        printf(" ");
      }
    }
    printf("\n");
  }
}
#include <stdio.h>

void draw_hollow_triangle(char symbol) {
  for (int i = 0; i < 5; i++) {
    for (int j = 0; j < 5 - i - 1; j++) {
      printf(" ");
    }

    if (i == 0) {
      printf("%c", symbol);
    } else if (i == 5 - 1) {
      for (int j = 0; j < (2 * i + 1); j++) {
        printf("%c", symbol);
      }
    } else {
      printf("%c", symbol);
      for (int j = 0; j < (2 * i - 1); j++) {
        printf(" ");
      }
      printf("%c", symbol);
    }
    printf("\n");
  }
}

int main() {
  char symbol;
  int height;

  printf("Enter a character: ");
  scanf(" %c", &symbol);

  draw_hollow_triangle(symbol);

  return 0;
}
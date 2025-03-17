#include <stdio.h>

void draw_top(int n) {
  for (int i = 0; i < n - 2; i++) {
    for (int j = 0; j < n - 2; j++) {
      printf(i % 2 == 0 ? "*" : "-");
    }
    printf("\\");
    printf(" /");
    for (int j = 0; j < n - 2; j++) {
      printf(i % 2 == 0 ? "*" : "-");
    }
    printf("\n");
  }
}

void draw_bottom(int n) {
  for (int i = 0; i < n - 2; i++) {
    for (int j = 0; j < n - 2; j++) {
      printf(i % 2 == 0 ? "*" : "-");
    }
    printf("/");
    printf(" \\");
    for (int j = 0; j < n - 2; j++) {
      printf(i % 2 == 0 ? "*" : "-");
    }
    printf("\n");
  }
}

void draw_butterfly(int n) {
  draw_top(n);

  for (int j = 0; j < n - 1; j++) {
    printf(" ");
  }
  printf("@\n");

  draw_bottom(n);
}

int main() {
  int n;
  scanf("%d", &n);
  draw_butterfly(n);
  return 0;
}
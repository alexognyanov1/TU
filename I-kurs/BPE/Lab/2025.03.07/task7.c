#include <stdio.h>

int sum(int *a, int *b) { return *a + *b; }
int diff(int *a, int *b) { return *a - *b; }
int product(int *a, int *b) { return *a * *b; }
int div(int *a, int *b) { return *a / *b; }

int main() {
  int a;
  int b;

  scanf("%d %d", &a, &b);

  printf("Sum: %d\n", sum(&a, &b));
  printf("Difference: %d\n", diff(&a, &b));
  printf("Product: %d\n", product(&a, &b));
  printf("Division: %d\n", div(&a, &b));
}
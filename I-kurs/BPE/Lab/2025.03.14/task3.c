#include <stdio.h>

int main() {
  int a = 5, b = 10;
  int *p1 = &a, *p2 = &b;

  printf("Before swap: a = %d, b = %d\n", a, b);

  *p1 = *p1 + *p2;
  *p2 = *p1 - *p2;
  *p1 = *p1 - *p2;

  printf("After swap: a = %d, b = %d\n", a, b);

  return 0;
}
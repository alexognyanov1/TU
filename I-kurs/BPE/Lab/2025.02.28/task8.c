#include <stdio.h>

void printFibonacci(int N) {
  int a = 1, b = 1, next;
  if (N >= 1) {
    printf("%d, ", a);
  }
  if (N >= 2) {
    printf("%d, ", b);
  }
  next = a + b;
  while (next <= N) {
    printf("%d, ", next);
    a = b;
    b = next;
    next = a + b;
  }
  printf("\n");
}

int main() {
  int N;
  printf("Enter a number N: ");
  scanf("%d", &N);
  printFibonacci(N);
  return 0;
}
#include <stdio.h>

int main() {
  int A, B, sum = 0;

  printf("Въведете две цели числа A и B: ");
  scanf("%d %d", &A, &B);

  for (int i = A; i <= B; i++) {
    if (i % 3 == 0) {
      sum += i;
    }
  }

  printf("Сумата на всички числа между %d и %d, които са кратни на 3, е: %d\n",
         A, B, sum);

  return 0;
}
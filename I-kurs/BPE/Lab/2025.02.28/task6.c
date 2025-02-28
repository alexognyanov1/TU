#include <stdio.h>

int main() {
  int N, maxDigit = 0;

  printf("Въведете число N: ");
  scanf("%d", &N);

  while (N > 0) {
    int digit = N % 10;
    if (digit > maxDigit) {
      maxDigit = digit;
    }
    N /= 10;
  }

  printf("Най-голямата цифра е %d\n", maxDigit);

  return 0;
}
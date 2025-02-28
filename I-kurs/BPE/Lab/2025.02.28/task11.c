#include <stdio.h>

int countDigits(int number) {
  int count = 0;
  if (number == 0) {
    return 1;
  }
  while (number != 0) {
    number /= 10;
    count++;
  }
  return count;
}

int main() {
  int number;
  printf("Enter a number: ");
  scanf("%d", &number);
  printf("Number of digits in %d is %d\n", number, countDigits(number));
  return 0;
}
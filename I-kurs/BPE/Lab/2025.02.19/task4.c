#include <stdio.h>

int main() {
  int number;
  printf("Enter a 4-digit number: ");
  scanf("%d", &number);

  int thousands = number / 1000;
  int hundreds = (number / 100) % 10;
  int tens = (number / 10) % 10;
  int units = number % 10;

  printf("%d\n", thousands);
  printf("%d\n", hundreds);
  printf("%d\n", tens);
  printf("%d\n", units);

  return 0;
}
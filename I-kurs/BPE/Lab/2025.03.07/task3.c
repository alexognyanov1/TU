#include <stdio.h>

int count_numbers(int number) {
  int count = 0;
  while (number > 0) {
    count++;
    number = number / 10;
  }
  return count;
}

int main() {
  int a;
  printf("Enter a number: ");
  scanf("%d", &a);

  printf("%d\n", count_numbers(a));

  return 0;
}
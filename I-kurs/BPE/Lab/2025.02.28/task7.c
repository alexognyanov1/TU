#include <stdio.h>

int main() {
  int number;
  int count = 0;
  int sum = 0;

  printf("Enter numbers (0 to stop):\n");

  while (1) {
    scanf("%d", &number);
    if (number == 0) {
      break;
    }
    sum += number;
    count++;
  }

  if (count > 0) {
    double average = (double)sum / count;
    printf("Count of numbers entered: %d\n", count);
    printf("Sum of numbers: %d\n", sum);
    printf("Average of numbers: %.2f\n", average);
  } else {
    printf("No numbers were entered.\n");
  }

  return 0;
}
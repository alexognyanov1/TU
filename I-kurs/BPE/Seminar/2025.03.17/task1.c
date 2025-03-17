#include <stdio.h>

int max(int a, int b) { return (a > b) ? a : b; }

int min(int a, int b) { return (a < b) ? a : b; }

int main() {
  int num, largest = 0, smallest = 0;
  int first = 1;

  while (1) {
    scanf("%d", &num);
    if (num == 0)
      break;
    if (first) {
      largest = smallest = num;
      first = 0;
    } else {
      largest = max(largest, num);
      smallest = min(smallest, num);
    }
  }

  printf("Largest: %d\n", largest);
  printf("Smallest: %d\n", smallest);

  return 0;
}
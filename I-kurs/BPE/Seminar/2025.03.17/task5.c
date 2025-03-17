#include <stdbool.h>
#include <stdio.h>

bool is_in_range(int a, int start, int end) { return a >= start && a <= end; }

int main() {
  int a, b, c;

  scanf("%d %d %d", &a, &b, &c);

  if (!is_in_range(a, 1, 50) || !is_in_range(b, 1, 50) ||
      !is_in_range(c, 1, 50)) {
    printf("Invalid input. Terminating.\n");
    return 1;
  }

  int sum = a + b + c;

  int minutes = sum / 60;
  int seconds = sum % 60;

  if (seconds < 10) {
    printf("%d:0%d\n", minutes, seconds);
  } else {
    printf("%d:%d\n", minutes, seconds);
  }
}
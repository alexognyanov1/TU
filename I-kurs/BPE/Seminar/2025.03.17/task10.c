#include <stdio.h>

int main() {
  int n, num;
  int count1 = 0, count2 = 0, count3 = 0, count4 = 0, count5 = 0;
  scanf("%d", &n);

  for (int i = 0; i < n; i++) {
    scanf("%d", &num);
    if (num < 200) {
      count1++;
    } else if (num < 400) {
      count2++;
    } else if (num < 600) {
      count3++;
    } else if (num < 800) {
      count4++;
    } else {
      count5++;
    }
  }

  printf("p1: %.2f%%\n", (count1 / (float)n) * 100);
  printf("p2: %.2f%%\n", (count2 / (float)n) * 100);
  printf("p3: %.2f%%\n", (count3 / (float)n) * 100);
  printf("p4: %.2f%%\n", (count4 / (float)n) * 100);
  printf("p5: %.2f%%\n", (count5 / (float)n) * 100);

  return 0;
}
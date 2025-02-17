#include <stdio.h>

int main() {
  double a, b, h, area;
  printf("Enter the length of the first base (a): ");
  scanf("%lf", &a);
  printf("Enter the length of the second base (b): ");
  scanf("%lf", &b);
  printf("Enter the height of the trapezoid (h): ");
  scanf("%lf", &h);

  area = ((a + b) / 2) * h;

  printf("The area of the trapezoid is: %.2lf\n", area);

  return 0;
}
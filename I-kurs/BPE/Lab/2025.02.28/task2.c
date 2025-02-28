#include <stdio.h>

int main() {
  double a, b, c;

  printf("Enter three numbers: ");
  scanf("%lf %lf %lf", &a, &b, &c);

  if (!(a + b > c && a + c > b && b + c > a)) {
    printf("The numbers cannot form a triangle.\n");
    return 0;
  }

  if (a == b && b == c) {
    printf("The triangle is equilateral.\n");
  } else if (a == b || a == c || b == c) {
    printf("The triangle is isosceles.\n");
  } else {
    printf("The triangle is scalene.\n");
  }

  return 0;
}
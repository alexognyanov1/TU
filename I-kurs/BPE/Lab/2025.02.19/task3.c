#include <math.h>
#include <stdio.h>

int main() {
  double radius;
  printf("Enter the radius of the circle: ");

  scanf("%lf", &radius);

  printf("The circumference of the circle is: %.2lf\n", 2 * M_PI * radius);

  return 0;
}
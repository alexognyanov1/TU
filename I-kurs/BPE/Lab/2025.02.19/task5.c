#include <math.h>
#include <stdio.h>

int main() {
  double radius, height, area, volume;

  printf("Enter the radius of the cylinder: ");
  scanf("%lf", &radius);
  printf("Enter the height of the cylinder: ");
  scanf("%lf", &height);

  area = 2 * M_PI * radius * (radius + height);
  volume = M_PI * radius * radius * height;

  printf("Surface Area of the cylinder: %.2lf\n", area);
  printf("Volume of the cylinder: %.2lf\n", volume);

  return 0;
}
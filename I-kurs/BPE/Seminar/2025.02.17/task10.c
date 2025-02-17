#include <math.h>
#include <stdio.h>

int main() {
  double angle;
  printf("Enter angle in degrees: ");
  scanf("%lf", &angle);

  double radians = angle * M_PI / 180.0;
  double sine = sin(radians);
  double cosine = cos(radians);
  double tangent = tan(radians);
  double cotangent = 1.0 / tangent;

  printf("sin(%.2f) = %.2f\n", angle, sine);
  printf("cos(%.2f) = %.2f\n", angle, cosine);
  printf("tan(%.2f) = %.2f\n", angle, tangent);
  printf("cot(%.2f) = %.2f\n", angle, cotangent);

  return 0;
}
#include <math.h>
#include <stdio.h>

int main() {
  float deg;
  printf("Enter degrees(float):\n");
  scanf("%f", &deg);

  float rad = deg * M_PI / 180;

  printf("Radians: %f\n", rad);
  return 0;
}
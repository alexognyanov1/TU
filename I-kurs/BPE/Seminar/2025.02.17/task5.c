#include <stdio.h>

int main() {
  float inches;
  printf("Enter inches(float):\n");
  scanf("%f", &inches);

  float m = inches / 39.37;
  float cm = m * 100;
  float mm = m * 1000;

  printf("Meters: %f\n", m);
  printf("Centimeters: %f\n", cm);
  printf("Milimeters: %f\n", mm);

  return 0;
}
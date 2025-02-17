#include <stdio.h>

int main() {
  float celcius;
  printf("Enter Celcius(float):\n");
  scanf("%f", &celcius);

  float f = (celcius * 9 / 5) + 32;

  printf("Farenheit: %f\n", f);
  return 0;
}
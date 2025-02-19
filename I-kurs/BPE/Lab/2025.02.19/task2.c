#include <stdio.h>

int main() {
  float a, b;

  printf("Enter the side length of the rectangle: ");
  scanf("%f %f", &a, &b);

  printf("The area of the square is: %.2f\n", a * b);

  return 0;
}
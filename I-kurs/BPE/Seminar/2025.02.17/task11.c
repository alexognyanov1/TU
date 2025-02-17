#include <stdio.h>
#include <stdlib.h>

typedef struct {
  int x;
  int y;
} Point;

int main() {
  Point A, B;
  printf("Enter coordinates of point A (x y): ");
  scanf("%d %d", &A.x, &A.y);
  printf("Enter coordinates of point B (x y): ");
  scanf("%d %d", &B.x, &B.y);

  int length = abs(A.x - B.x);
  int width = abs(A.y - B.y);
  int area = length * width;

  printf("The area of the rectangle is: %d\n", area);
  return 0;
}
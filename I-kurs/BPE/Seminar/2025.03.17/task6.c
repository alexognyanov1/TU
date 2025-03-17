#include <stdio.h>

typedef struct {
  int x;
  int y;
} Point;

int isPointInsideRectangle(Point p, Point topLeft, Point bottomRight) {
  if (p.x >= topLeft.x && p.x <= bottomRight.x && p.y >= topLeft.y &&
      p.y <= bottomRight.y) {
    return 1;
  }
  return 0;
}

int main() {
  Point p, topLeft, bottomRight;

  printf("Enter the coordinates of the point (x y): ");
  scanf("%d %d", &p.x, &p.y);

  printf(
      "Enter the coordinates of the top-left point of the rectangle (x y): ");
  scanf("%d %d", &topLeft.x, &topLeft.y);

  printf("Enter the coordinates of the bottom-right point of the rectangle (x "
         "y): ");
  scanf("%d %d", &bottomRight.x, &bottomRight.y);

  if (isPointInsideRectangle(p, topLeft, bottomRight)) {
    printf("The point is inside the rectangle.\n");
  } else {
    printf("The point is outside the rectangle.\n");
  }

  return 0;
}
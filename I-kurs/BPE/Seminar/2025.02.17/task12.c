#include <math.h>
#include <stdio.h>

typedef struct {
  double x;
  double y;
} Point;

double calculateArea(Point a, Point b, Point c) {
  return fabs((a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)) /
              2.0);
}

int main() {
  Point a, b, c;
  printf("Enter coordinates of point A (x y): ");
  scanf("%lf %lf", &a.x, &a.y);
  printf("Enter coordinates of point B (x y): ");
  scanf("%lf %lf", &b.x, &b.y);
  printf("Enter coordinates of point C (x y): ");
  scanf("%lf %lf", &c.x, &c.y);

  double area = calculateArea(a, b, c);
  printf("The area of the triangle is: %.2lf\n", area);

  return 0;
}
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define MIN_CAPACITY 10

typedef struct {
  int x;
  int y;
} Point;

Point scanPoint() {
  int x, y;

  scanf("%d %d", &x, &y);

  Point p;
  p.x = x;
  p.y = y;

  return p;
}

void appendPoint(Point *points, int *len, int *capacity, Point p) {
  if (len >= capacity) {
    *capacity *= 2;
    points = realloc(points, *len * 2);
  }

  points[*len] = p;
  *len += 1;
}

int main() {
  Point *points = malloc(sizeof(Point) * MIN_CAPACITY);
  int capacity = MIN_CAPACITY;
  int len = 0;

  for (int i = 0; i < 3; i++) {
    Point p = scanPoint();
    appendPoint(points, &len, &capacity, p);
  }

  for (int i = 0; i < len - 1; i++) {
    printf("Distance between points at index %d and %d: %f\n", i, i + 1,
           sqrt(pow(abs(points[i].x - points[i + 1].x), 2) +
                pow(abs(points[i].y - points[i + 1].y), 2)));
  }

  printf("Distance between points at index %d and 0: %f\n", len - 1,
         sqrt(pow(abs(points[0].x - points[len - 1].x), 2) +
              pow(abs(points[0].y - points[len - 1].y), 2)));

  free(points);
}
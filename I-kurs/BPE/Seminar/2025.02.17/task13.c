#include <stdio.h>

int main() {
  float w, h;
  scanf("%f %f", &w, &h);

  int width_cm = (int)(w * 100);
  int height_cm = (int)(h * 100);

  int desk_width = 70;
  int desk_height = 120;
  int corridor_width = 100;

  int desks_per_row = (width_cm - corridor_width) / desk_width;
  int rows = height_cm / desk_height;

  int total_desks = desks_per_row * rows - 3;

  printf("%d\n", total_desks);

  return 0;
}
#include <stdio.h>

int main() {
  double N, W, L, M, O;

  printf("Enter the side length of the square (N): ");
  scanf("%lf", &N);

  printf("Enter the width of a tile (W): ");
  scanf("%lf", &W);

  printf("Enter the length of a tile (L): ");
  scanf("%lf", &L);

  printf("Enter the width of the bench (M): ");
  scanf("%lf", &M);

  printf("Enter the length of the bench (O): ");
  scanf("%lf", &O);

  double area_square = N * N;
  double area_bench = M * O;
  double area_tile = W * L;
  double area_to_cover = area_square - area_bench;

  double tiles_needed = area_to_cover / area_tile;
  double time_needed = tiles_needed * 0.2;

  printf("Tiles needed: %.2f\n", tiles_needed);
  printf("Time needed: %.2f\n", time_needed);

  return 0;
}
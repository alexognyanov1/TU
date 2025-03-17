#include <stdio.h>

int main() {
  double X, Y, Z;
  int workers;

  printf("Enter the area of the vineyard in square meters: ");
  scanf("%lf", &X);
  printf("Enter the amount of grapes per square meter: ");
  scanf("%lf", &Y);
  printf("Enter the desired amount of wine in liters: ");
  scanf("%lf", &Z);
  printf("Enter the number of workers: ");
  scanf("%d", &workers);

  double totalGrapes = X * Y;
  double grapesForWine = totalGrapes * 0.40;
  double wineProduced = grapesForWine / 2.5;

  if (wineProduced >= Z) {
    double surplusWine = wineProduced - Z;
    double winePerWorker = surplusWine / workers;
    printf("Total wine: %.2f liters\n", wineProduced);
    printf("%.2f liters left -> %.2f liters per person.\n", surplusWine,
           winePerWorker);
  } else {
    double wineShortage = Z - wineProduced;
    printf("%.2f liters wine needed.\n", wineShortage);
  }

  return 0;
}
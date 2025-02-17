#include <stdio.h>

int main() {
  float vegPrice, fruitPrice;
  int vegKg, fruitKg;
  float totalBGN, totalEUR;

  scanf("%f", &vegPrice);
  scanf("%f", &fruitPrice);
  scanf("%d", &vegKg);
  scanf("%d", &fruitKg);

  totalBGN = (vegPrice * vegKg) + (fruitPrice * fruitKg);
  totalEUR = totalBGN / 1.95;

  printf("%.2f\n", totalEUR);

  return 0;
}
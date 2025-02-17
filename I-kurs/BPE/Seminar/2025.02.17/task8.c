#include <stdio.h>

#define USD_RATE 0.58
#define EUR_RATE 0.51
#define GBP_RATE 0.44

int main() {
  double leva;
  double usd, eur, gbp;

  printf("Enter amount in leva: ");
  scanf("%lf", &leva);

  usd = leva * USD_RATE;
  eur = leva * EUR_RATE;
  gbp = leva * GBP_RATE;

  printf("%.2lf leva is equivalent to:\n", leva);
  printf("%.2lf USD\n", usd);
  printf("%.2lf EUR\n", eur);
  printf("%.2lf GBP\n", gbp);

  return 0;
}
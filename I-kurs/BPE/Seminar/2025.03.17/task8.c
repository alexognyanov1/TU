#include <stdio.h>

int main() {
  double V, flowRate1, flowRate2, N;

  printf("Enter the volume of the pool (in cubic meters): ");
  scanf("%lf", &V);
  printf("Enter the flow rate of the first pipe (in liters per hour): ");
  scanf("%lf", &flowRate1);
  printf("Enter the flow rate of the second pipe (in liters per hour): ");
  scanf("%lf", &flowRate2);
  printf("Enter the time the worker will be absent (in hours): ");
  scanf("%lf", &N);

  flowRate1 /= 1000;
  flowRate2 /= 1000;

  double totalWater = (flowRate1 + flowRate2) * N;

  if (totalWater > V) {
    printf("After %.2f hours, the pool will overflow with %.2f cubic meters of "
           "water.\n",
           N, totalWater - V);
  } else {
    printf("After %.2f hours, the pool will be filled to %.2f%%.\n", N,
           (totalWater / V) * 100);
  }

  return 0;
}
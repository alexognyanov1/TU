#include <stdbool.h>
#include <stdio.h>

float calculatePrice(int n, float start, float day, float night,
                     int minDistance, bool isNight) {
  if (n >= minDistance) {
    return start + (n * (isNight ? night : day));
  }

  return -1.0;
}

float findCheapest(float *arr) {
  float min = arr[0];
  for (int i = 0; i < 3; i++) {
    if (arr[i] >= 0 && min > arr[i]) {
      min = arr[i];
    }
  }

  return min;
}

int main() {
  float taxiStart = 0.7;
  float taxiDay = 0.79;
  float taxiNight = 0.9;

  float bus = 0.09;
  int busMinDistance = 20;

  float train = 0.06;
  int trainMinDistance = 100;

  int n;
  char time_of_day;
  scanf("%d %c", &n, &time_of_day);

  if (time_of_day != 'N' && time_of_day != 'D') {
    printf("Invalid time of day. Terminating\n");
    return 1;
  }

  float priceTaxi =
      calculatePrice(n, taxiStart, taxiDay, taxiNight, 0, time_of_day == 'N');
  float priceBus = calculatePrice(n, 0, bus, bus, 20, time_of_day == 'N');
  float priceTrain =
      calculatePrice(n, 0, train, train, 100, time_of_day == 'N');

  float prices[3] = {priceTaxi, priceBus, priceTrain};

  float cheapest = findCheapest(&prices[0]);

  printf("%f\n", cheapest);
}
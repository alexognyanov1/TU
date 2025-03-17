#include <stdio.h>

int main() {
  int hour;
  int minutes;
  char minutesZero;

  scanf("%d %d", &hour, &minutes);

  minutes += 15;

  if (minutes > 60) {
    minutes = minutes % 60;
    hour++;
  }

  if (hour > 23) {
    hour = hour % 24;
  }

  if (minutes < 10) {
    printf("%d:0%d", hour, minutes);
  } else {
    printf("%d:%d", hour, minutes);
  }
  printf("\n");
}
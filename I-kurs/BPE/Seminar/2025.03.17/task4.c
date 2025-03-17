#include <stdio.h>

int main() {
  int points;
  double bonusPoints = 0;

  printf("Enter points: ");
  scanf("%d", &points);

  if (points <= 100) {
    bonusPoints = 5;
  } else if (points > 100 && points <= 1000) {
    bonusPoints = points * 0.20;
  } else if (points > 1000) {
    bonusPoints = points * 0.10;
  }

  if (points % 2 == 0) {
    bonusPoints += 1;
  } else if (points % 10 == 5) {
    bonusPoints += 2;
  }

  double totalPoints = points + bonusPoints;

  printf("Bonus points: %.2f\n", bonusPoints);
  printf("Total points: %.2f\n", totalPoints);

  return 0;
}
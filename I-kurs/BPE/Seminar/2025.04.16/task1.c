#include <stdio.h>
#include <string.h>

int main() {
  int guests;
  printf("Enter the number of guests: ");
  scanf("%d", &guests);

  double totalCost = 0.0;
  int chairs = 0, tables = 0, cups = 0, placeSettings = 0;

  char input[50];
  while (1) {
    printf("Enter item or 'PARTY!': ");
    scanf("%s", input);

    if (strcmp(input, "PARTY!") == 0) {
      break;
    }

    if (strcmp(input, "Chair") == 0) {
      chairs++;
      totalCost += 13.99;
    } else if (strcmp(input, "Table") == 0) {
      tables++;
      totalCost += 42.00;
    } else if (strcmp(input, "Cups") == 0) {
      cups += 6;
      totalCost += 5.98;
    } else if (strcmp(input, "Place-setting") == 0) {
      placeSettings++;
      totalCost += 21.02;
    }
  }

  printf("Value: %.2f\n", totalCost);

  int neededChairs = guests - chairs;
  int neededTables = (guests + 7) / 8 - tables;
  int neededCups = guests - cups;
  int neededPlaceSettings = guests - placeSettings;

  if (neededTables > 0) {
    printf("%d table%s needed\n", neededTables, neededTables > 1 ? "s" : "");
  }
  if (neededChairs > 0) {
    printf("%d chair%s needed\n", neededChairs, neededChairs > 1 ? "s" : "");
  }
  if (neededCups > 0) {
    printf("%d cup%s needed\n", neededCups, neededCups > 1 ? "s" : "");
  }
  if (neededPlaceSettings > 0) {
    printf("%d place-setting%s needed\n", neededPlaceSettings,
           neededPlaceSettings > 1 ? "s" : "");
  }
}
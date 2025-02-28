#include <stdio.h>

int main() {
  int month;
  printf("Въведете число от 1 до 12: ");
  if (scanf("%d", &month) != 1 || month < 1 || month > 12) {
    printf("Невалидно число.\n");
    return 1;
  }

  switch (month) {
  case 1:
    printf("Януари (Зима)\n");
    break;
  case 2:
    printf("Февруари (Зима)\n");
    break;
  case 3:
    printf("Март (Пролет)\n");
    break;
  case 4:
    printf("Април (Пролет)\n");
    break;
  case 5:
    printf("Май (Пролет)\n");
    break;
  case 6:
    printf("Юни (Лято)\n");
    break;
  case 7:
    printf("Юли (Лято)\n");
    break;
  case 8:
    printf("Август (Лято)\n");
    break;
  case 9:
    printf("Септември (Есен)\n");
    break;
  case 10:
    printf("Октомври (Есен)\n");
    break;
  case 11:
    printf("Ноември (Есен)\n");
    break;
  case 12:
    printf("Декември (Зима)\n");
    break;
  }

  return 0;
}
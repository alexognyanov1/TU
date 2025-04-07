#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 10

typedef struct {
  char name[56];
  char id[7];
  double price;
  int code;
} User;

FILE *createFileIfNotExists(char *filename) {
  FILE *file;
  file = fopen(filename, "r");

  if (file == NULL) {
    file = fopen(filename, "w");

    return file;
  } else {
    file = fopen(filename, "a");
  }

  return file;
}

void printUsers(User *users, int len) {
  for (int i = 0; i < len; i++) {
    printf("\n");
    printf("Name: %s\n", users[i].name);
    printf("Id: %s\n", users[i].id);
    printf("Price: %.2lf\n", users[i].price);
    printf("Code: %d\n", users[i].code);
  }
}

void appendUser(User *users, int *len, int *capacity, User user) {
  if (len >= capacity) {
    User *temp = realloc(users, sizeof(User) * (*len + 1));
    if (!temp) {
      printf("Failed to realloc");
      return;
    }
    users = temp;
    *capacity += 1;
    *len += 1;
  } else {
    users[*len] = user;
    *len += 1;
  }
}

void getUserAndAppend(FILE *file, User *users, int *len, int *capacity) {
  char name[56];
  char id[7];
  double price;
  int code;

  printf("Name: ");
  fgets(name, 56, stdin);

  if ((strlen(name) > 0) && (name[strlen(name) - 1] == '\n')) {
    name[strlen(name) - 1] = '\0';
  }

  printf("ID: ");
  scanf("%s", id);

  printf("Price: ");
  scanf("%lf", &price);

  printf("Code: ");
  scanf("%d", &code);

  int ch;
  while ((ch = getchar()) != '\n' && ch != EOF) {
  }

  User newUser;

  strcpy(newUser.name, name);
  strcpy(newUser.id, id);
  newUser.price = price;
  newUser.code = code;

  appendUser(users, len, capacity, newUser);

  size_t nameLength = strlen(newUser.name);

  fprintf(file, "%zu;%s;%s;%.2lf;%d\n", nameLength, newUser.name, newUser.id,
          newUser.price, newUser.code);
}

void underAveragePrice(User *users, int len) {
  double sum = 0;

  for (int i = 0; i < len; i++) {
    sum += users[i].price;
  }

  double avg = sum / len;

  for (int i = 0; i < len; i++) {
    if (users[i].price < avg) {
      printf("%s - %s - %.2lf\n", users[i].name, users[i].id, users[i].price);
    }
  }
}

int main() {
  User *users = malloc(sizeof(User) * INITIAL_CAPACITY);
  int capacity = INITIAL_CAPACITY;
  int len = 0;

  char filename[] = "membersText.txt";

  FILE *file = createFileIfNotExists(filename);

  for (int i = 0; i < 3; i++) {
    getUserAndAppend(file, users, &len, &capacity);
  }

  printUsers(users, len);

  underAveragePrice(users, len);

  if (len > 0) {
    free(users);
  }

  return 0;
}
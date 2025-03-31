#include <stdio.h>
#include <stdlib.h>

#define MAX_N 100000

typedef struct Node {
  struct Node **children;
  int childCount;
} Node;

Node *adjacencyList[MAX_N + 1];

void addFriend(int personIndex, int friendIndex) {
  if (adjacencyList[personIndex] == NULL) {
    adjacencyList[personIndex] = (Node *)malloc(sizeof(Node));
    adjacencyList[personIndex]->children = NULL;
    adjacencyList[personIndex]->childCount = 0;
  }

  if (adjacencyList[friendIndex] == NULL) {
    adjacencyList[friendIndex] = (Node *)malloc(sizeof(Node));
    adjacencyList[friendIndex]->children = NULL;
    adjacencyList[friendIndex]->childCount = 0;
  }

  Node *person = adjacencyList[personIndex];
  for (int i = 0; i < person->childCount; i++) {
    if (person->children[i] == adjacencyList[friendIndex]) {
      return;
    }
  }
  person->children = (Node **)realloc(
      person->children, (person->childCount + 1) * sizeof(Node *));
  person->children[person->childCount] = adjacencyList[friendIndex];
  person->childCount++;
}

int countFriends(int personIndex) {
  if (adjacencyList[personIndex] == NULL) {
    return 0;
  }

  return adjacencyList[personIndex]->childCount;
}

void freeMemory() {
  for (int i = 1; i <= MAX_N; i++) {
    Node *current = adjacencyList[i];
    if (current) {
      free(current->children);
      free(current);
    }
  }
}

int main() {
  int m, a, b, q;
  scanf("%d", &m);
  for (int i = 0; i < m; i++) {
    scanf("%d %d", &a, &b);
    addFriend(a, b);
    addFriend(b, a);
  }
  printf("Enter desired person number: ");
  scanf("%d", &q);
  printf("%d\n", countFriends(q));
  freeMemory();
  return 0;
}
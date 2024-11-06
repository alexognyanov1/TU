// Description: This script implements a doubly linked list with functions to create, append, and traverse the list.
// Tags: Lab, C, Linked List, Data Structures

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct linkedListNode LinkedListNode;

struct linkedListNode {
  int data;
  LinkedListNode* next;
  LinkedListNode* prev;
};

typedef struct linkedList {
  LinkedListNode* head;
  LinkedListNode* tail;
} LinkedList;

LinkedList* createLinkedList(int data){
  LinkedListNode* node = (LinkedListNode*)malloc(sizeof(LinkedListNode));
  node->data = data;
  node->next = NULL;
  node->prev = NULL;

  LinkedList* list = (LinkedList*)malloc(sizeof(LinkedList));
  list->head = node;
  list->tail = node;

  return list;
}

void appendToLinkedList(LinkedList* list, int data){
  LinkedListNode* node = (LinkedListNode*)malloc(sizeof(LinkedListNode));
  node->data = data;
  node->prev = list->tail;
  node->next = NULL;

  list->tail->next = node;
  list->tail = node;
}

void traverseAndPrintLinkedList(LinkedList* list, bool backwards){
  LinkedListNode* node = backwards == false ? list->head : list->tail;

  while(node != NULL) {
    printf("%d ", node->data);
    if(backwards == false){
      node = node->next;
    }else{
      node = node->prev;
    }
  }
  
  printf("\n");
}

int main(){
    LinkedList* l = createLinkedList(1);

    appendToLinkedList(l, 2);
    appendToLinkedList(l, 3);
    
    traverseAndPrintLinkedList(l, false);
    traverseAndPrintLinkedList(l, true);

    return 0;
}
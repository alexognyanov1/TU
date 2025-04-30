#include <stdio.h>
#include <string.h>

struct Product {
  char name[50];
  float price;
  int id;
};

struct Order {
  char address[50];
  int product_id;
};

int main() {
  struct Product products[100];
  int product_count = 0;
  char command[50];

  printf("Enter command: (Product or Order | END)\n");

  while (1) {
    scanf("%s", command);

    if (strcmp(command, "Product") == 0) {
      if (product_count >= 100) {
        printf("Product list is full!\n");
        continue;
      }

      struct Product product;
      printf("Enter product name: ");
      scanf("%s", product.name);
      printf("Enter product price: ");
      scanf("%f", &product.price);
      printf("Enter product id: ");
      scanf("%d", &product.id);

      products[product_count++] = product;
      printf("Product added successfully!\n");

    } else if (strcmp(command, "Order") == 0) {
      struct Order order;
      printf("Enter order address: ");
      while (getchar() != '\n')
        ;
      fgets(order.address, sizeof(order.address), stdin);
      order.address[strcspn(order.address, "\n")] = '\0';
      printf("Enter product id: ");
      scanf("%d", &order.product_id);

      int found = 0;
      for (int i = 0; i < product_count; i++) {
        if (products[i].id == order.product_id) {
          printf("Order fulfilled for product '%s' at address '%s'.\n",
                 products[i].name, order.address);
          found = 1;
          break;
        }
      }

      if (!found) {
        printf("Order wasn't fulfilled. No product with ID %d found.\n",
               order.product_id);
      }

    } else if (strcmp(command, "END") == 0) {
      printf("Exiting...\n");
      return 0;

    } else {
      printf("Invalid command. Please enter 'Product', 'Order', or 'END'.\n");
    }
  }

  return 0;
}
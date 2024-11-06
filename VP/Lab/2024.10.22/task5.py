# Description: This script manages orders, prints the number of unique products, and lists usernames for a product.
# Tags: Orders, List Operations

class OrderManager:
    orders = []

    def add_order(self, id: int, user: str, product: str):
        self.orders.append({"id": id, "user": user, "product": product})

    def print_number_of_unique_products(self):
        print(len(set([order['product'] for order in self.orders])))

    def print_usernames_for_product(self, product: str, alpabetical: bool = False):
        users = [order['user']
                 for order in self.orders if order['product'] == product]

        print(sorted(users) if alpabetical else users)


orderManager = OrderManager()

orderManager.add_order(2, 'user2', 'product1')
orderManager.add_order(1, 'user1', 'product1')
orderManager.add_order(3, 'user1', 'product2')


orderManager.print_number_of_unique_products()

orderManager.print_usernames_for_product('product1')
orderManager.print_usernames_for_product('product1', True)

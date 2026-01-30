package task2;

import java.util.Arrays;
import java.util.List;

public class Task2Runner {
    public static void run() {
        List<Product> products = Arrays.asList(
                new Product("Laptop", 1200.0, "Electronics"),
                new Product("Headphones", 150.0, "Electronics"),
                new Product("Desk", 300.0, "Furniture"),
                new Product("Chair", 180.0, "Furniture"),
                new Product("Smartphone", 900.0, "Electronics"),
                new Product("Lamp", 60.0, "Furniture")
        );
        List<Product> electronics = ProductProcessor.getProductsByCategory(products, "Electronics");
        List<Product> expensive = ProductProcessor.getExpensiveProducts(products, 200.0);
        System.out.println("Products in category Electronics sorted by price:");
        electronics.forEach(System.out::println);
        System.out.println("Products more expensive than 200 sorted by price descending:");
        expensive.forEach(System.out::println);
    }
}

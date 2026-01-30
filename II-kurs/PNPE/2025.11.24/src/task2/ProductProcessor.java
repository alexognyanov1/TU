package task2;

import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class ProductProcessor {
    public static List<Product> getProductsByCategory(List<Product> products, String category) {
        return products.stream()
                .filter(product -> product.getCategory().equalsIgnoreCase(category))
                .sorted(Comparator.comparingDouble(Product::getPrice))
                .collect(Collectors.toList());
    }

    public static List<Product> getExpensiveProducts(List<Product> products, double minPrice) {
        return products.stream()
                .filter(product -> product.getPrice() > minPrice)
                .sorted(Comparator.comparingDouble(Product::getPrice).reversed())
                .collect(Collectors.toList());
    }
}

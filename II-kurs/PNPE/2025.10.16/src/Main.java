import Task2.Car;

import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        System.out.println("\n=== TASK 2: CAR ===");
        List<Car> cars = new ArrayList<>();
        cars.add(new Car("Audi", "A4", "Black", 190, "Diesel", "Automatic", 2019));
        cars.add(new Car("BMW", "X5", "White", 250, "Petrol", "Automatic", 2021));
        cars.add(new Car("Alfa Romeo", "Giulia", "Red", 200, "Petrol", "Manual", 2020));
        cars.add(new Car("Audi", "A4", "Black", 190, "Diesel", "Automatic", 2019)); // duplicate

        System.out.println("Original list:");
        cars.forEach(System.out::println);

        System.out.println("\nCars starting with 'A':");
        Car.filterByFirstLetter(cars, 'A').forEach(System.out::println);

        System.out.println("\nCars sorted ascending by brand:");
        Car.sortByBrand(cars, true).forEach(System.out::println);

        System.out.println("\nCars sorted descending by brand:");
        Car.sortByBrand(cars, false).forEach(System.out::println);

        System.out.println("\nAfter removing duplicates:");
        Car.removeDuplicates(cars).forEach(System.out::println);
    }
}
package app;

import task1.Task1Runner;
import task2.Task2Runner;
import task3.Task3Runner;
import task4.Task4Runner;
import task5.Task5Runner;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Choose a task to run (1-5):");
        System.out.println("1 - Filter numbers");
        System.out.println("2 - Filter and sort products");
        System.out.println("3 - Student statistics");
        System.out.println("4 - Transform words");
        System.out.println("5 - Apply string transforms");
        String choice = scanner.nextLine().trim();
        switch (choice) {
            case "1":
                Task1Runner.run();
                break;
            case "2":
                Task2Runner.run();
                break;
            case "3":
                Task3Runner.run();
                break;
            case "4":
                Task4Runner.run();
                break;
            case "5":
                Task5Runner.run();
                break;
            default:
                System.out.println("No task selected.");
        }
    }
}

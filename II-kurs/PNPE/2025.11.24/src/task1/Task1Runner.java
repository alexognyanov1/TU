package task1;

import java.util.Arrays;
import java.util.List;

public class Task1Runner {
    public static void run() {
        List<Integer> numbers = Arrays.asList(5, 12, 8, 20, 13, 14);
        List<Integer> filtered = NumberFilter.getEvenNumbersGreaterThan10(numbers);
        System.out.println("Original numbers: " + numbers);
        System.out.println("Even numbers greater than 10 sorted: " + filtered);
    }
}

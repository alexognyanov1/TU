package task1;

import java.util.List;
import java.util.stream.Collectors;

public class NumberFilter {
    public static List<Integer> getEvenNumbersGreaterThan10(List<Integer> numbers) {
        return numbers.stream()
                .filter(number -> number % 2 == 0)
                .filter(number -> number > 10)
                .sorted()
                .collect(Collectors.toList());
    }
}

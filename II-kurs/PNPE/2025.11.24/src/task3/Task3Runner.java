package task3;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.OptionalDouble;

public class Task3Runner {
    public static void run() {
        List<Student> students = Arrays.asList(
                new Student("Alex", 20, 5.80),
                new Student("Maria", 21, 5.20),
                new Student("Ivan", 19, 4.40),
                new Student("Sofia", 22, 6.00),
                new Student("Peter", 20, 5.00)
        );
        OptionalDouble average = StudentStatistics.getAverageGrade(students);
        if (average.isPresent()) {
            System.out.println("Average grade: " + average.getAsDouble());
        } else {
            System.out.println("Average grade: N/A");
        }
        Map<Boolean, List<Student>> partition = StudentStatistics.partitionByPass(students, 5.0);
        System.out.println("Passed:");
        partition.get(true).forEach(System.out::println);
        System.out.println("Not passed:");
        partition.get(false).forEach(System.out::println);
        List<String> aboveAverageNames = StudentStatistics.getNamesAboveAverage(students);
        System.out.println("Students above average grade sorted by name:");
        aboveAverageNames.forEach(System.out::println);
    }
}

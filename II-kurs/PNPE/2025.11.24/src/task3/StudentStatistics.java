package task3;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.OptionalDouble;
import java.util.stream.Collectors;

public class StudentStatistics {
    public static OptionalDouble getAverageGrade(List<Student> students) {
        return students.stream()
                .mapToDouble(Student::getGrade)
                .average();
    }

    public static Map<Boolean, List<Student>> partitionByPass(List<Student> students, double passGrade) {
        return students.stream()
                .collect(Collectors.partitioningBy(student -> student.getGrade() >= passGrade));
    }

    public static List<String> getNamesAboveAverage(List<Student> students) {
        OptionalDouble average = getAverageGrade(students);
        if (average.isEmpty()) {
            return Collections.emptyList();
        }
        double value = average.getAsDouble();
        return students.stream()
                .filter(student -> student.getGrade() > value)
                .map(Student::getName)
                .sorted()
                .collect(Collectors.toList());
    }
}

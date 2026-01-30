package task4;

import java.util.Arrays;
import java.util.List;

public class Task4Runner {
    public static void run() {
        List<String> words = Arrays.asList("java", "stream", "lambda", "code", "lambda", "programming");
        List<String> transformed = WordTransformer.transformWords(words);
        System.out.println("Original words: " + words);
        System.out.println("Transformed words:");
        transformed.forEach(System.out::println);
    }
}

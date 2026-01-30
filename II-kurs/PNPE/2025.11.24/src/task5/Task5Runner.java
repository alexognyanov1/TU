package task5;

import java.util.Arrays;
import java.util.List;

public class Task5Runner {
    public static void run() {
        List<String> words = Arrays.asList("hello", "java", "Stream", "API");
        List<String> uppercased = TextTransformer.applyTransform(words, text -> text.toUpperCase());
        List<String> withPrefix = TextTransformer.applyTransform(words, text -> ">> " + text);
        List<String> firstThree = TextTransformer.applyTransform(words, text -> text.length() >= 3 ? text.substring(0, 3) : text);
        System.out.println("Original words: " + words);
        System.out.println("Uppercased:");
        uppercased.forEach(System.out::println);
        System.out.println("With prefix:");
        withPrefix.forEach(System.out::println);
        System.out.println("First three characters:");
        firstThree.forEach(System.out::println);
    }
}

import java.util.Arrays;
import java.util.Comparator;

public class Task5 {
    public static void main(String[] args) {
        String[] words = {"apple", "kiwi", "banana", "pear", "plum"};
        Arrays.sort(words, Comparator.comparingInt(String::length));
        for (String word : words) {
            System.out.println(word);
        }
    }
}

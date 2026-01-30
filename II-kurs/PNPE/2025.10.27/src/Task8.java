import java.util.LinkedHashSet;
import java.util.Set;

public class Task8 {
    public static void main(String[] args) {
        int[] first = {1, 2, 3, 4, 5, 6};
        int[] second = {4, 5, 6, 7, 8};
        Set<Integer> common = new LinkedHashSet<>();
        for (int value : first) {
            for (int other : second) {
                if (value == other) {
                    common.add(value);
                    break;
                }
            }
        }
        if (common.isEmpty()) {
            System.out.println("No common elements");
        } else {
            for (int value : common) {
                System.out.println(value);
            }
        }
    }
}

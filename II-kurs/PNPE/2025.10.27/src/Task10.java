import java.util.Arrays;

public class Task10 {
    public static int[] removeAll(int[] arr, int target) {
        int count = 0;
        for (int value : arr) {
            if (value != target) {
                count++;
            }
        }
        int[] result = new int[count];
        int index = 0;
        for (int value : arr) {
            if (value != target) {
                result[index++] = value;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 2, 4, 2, 5};
        int[] filtered = removeAll(numbers, 2);
        System.out.println(Arrays.toString(filtered));
    }
}

public class Task4 {
    public static int sum(int[] arr) {
        int total = 0;
        for (int number : arr) {
            total += number;
        }
        return total;
    }

    public static void main(String[] args) {
        int[] numbers = {2, 4, 6, 8, 10};
        System.out.println("Sum: " + sum(numbers));
    }
}

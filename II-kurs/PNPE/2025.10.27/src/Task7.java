public class Task7 {
    public static void main(String[] args) {
        int[] numbers = {3, -2, -5, 6, 0, 4, -1, 9};
        int positives = 0;
        int negatives = 0;
        for (int number : numbers) {
            if (number > 0) {
                positives++;
            } else if (number < 0) {
                negatives++;
            }
        }
        System.out.println("Positive count: " + positives);
        System.out.println("Negative count: " + negatives);
    }
}

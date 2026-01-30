import java.util.Scanner;

public class Task14 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        while (true) {
            long n = sc.nextLong();
            if (n % 10 == 0) {
                System.out.println(n);
                break;
            } else {
                System.out.println("Invalid number, please enter a new number.");
            }
        }
    }
}
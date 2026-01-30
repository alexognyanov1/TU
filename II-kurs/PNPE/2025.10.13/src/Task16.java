import java.util.Scanner;

public class Task16 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        long n = sc.nextLong();
        if (n >= 1 && n % 5 == 0) System.out.println("Valid!");
        else System.out.println("Invalid!");
    }
}
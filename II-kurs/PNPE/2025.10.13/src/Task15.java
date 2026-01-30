import java.util.Scanner;

public class Task15 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int h = sc.nextInt(), m = sc.nextInt();
        int total = h * 60 + m + 15;
        total %= 24 * 60;
        int nh = total / 60, nm = total % 60;
        System.out.printf("%d:%02d%n", nh, nm);
    }
}
import java.util.Scanner;

public class Task05 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        System.out.println(n != 0 && n >= -100 && n <= 100 ? "Yes" : "No");
    }
}
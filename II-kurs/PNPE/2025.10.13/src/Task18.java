import java.math.BigInteger;
import java.util.Scanner;

public class Task18 {
    private static BigInteger factRange(int fromInclusive, int toInclusive) {
        BigInteger r = BigInteger.ONE;
        for (int i = fromInclusive; i <= toInclusive; i++) r = r.multiply(BigInteger.valueOf(i));
        return r;
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int N = sc.nextInt(), K = sc.nextInt();
        if (N < 0 || K < 0 || K > N) {
            System.out.println("Invalid input");
            return;
        }
        BigInteger part = factRange(Math.max(1, N - K + 1), N);
        BigInteger kfact = factRange(1, K);
        System.out.println(part.multiply(kfact).toString());
    }
}
import java.math.BigInteger;
import java.util.Scanner;

public class Task17 {
    private static BigInteger factRange(int fromInclusive, int toInclusive) {
        BigInteger r = BigInteger.ONE;
        for (int i = fromInclusive; i <= toInclusive; i++) r = r.multiply(BigInteger.valueOf(i));
        return r;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int N = sc.nextInt(), K = sc.nextInt();
        if (K <= 1 || K>= N) {
            System.out.println("Invalid input");
            return;
        }
        BigInteger result = factRange(K + 1, N);
        System.out.println(result.toString());
    }
}

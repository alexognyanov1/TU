import java.util.Locale;
import java.util.Scanner;

public class Task20 {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner sc = new Scanner(System.in);
        String type = sc.next().trim();
        double area;
        switch (type) {
            case "square": {
                double a = sc.nextDouble();
                area = a * a; break;
            }
            case "rectangle": {
                double a = sc.nextDouble(), b = sc.nextDouble();
                area = a * b; break;
            }
            case "circle": {
                double r = sc.nextDouble();
                area = Math.PI * r * r; break;
            }
            case "triangle": {
                double a = sc.nextDouble(), h = sc.nextDouble();
                area = a * h / 2.0; break;
            }
            default:
                System.out.println("Error");
                return;
        }
        System.out.printf("%.3f%n", area);
    }
}
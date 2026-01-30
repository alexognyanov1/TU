import java.util.Locale;
import java.util.Scanner;

public class Task19 {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner sc = new Scanner(System.in);
        double budget = sc.nextDouble();
        if(budget < 1 || budget > 1000000){
            System.out.println("Invalid budget");
            System.exit(1);
        }
        int stat = sc.nextInt();
        if(stat < 1 || stat > 500){
            System.out.println("Invalid stat");
            System.exit(1);
        }
        double pricePerCostume = sc.nextDouble();
        if(pricePerCostume < 1 || pricePerCostume > 1000000){
            System.out.println("Invalid pricePerCostume");
            System.exit(1);
        }

        double decor = budget * 0.10;
        double costumes = stat * pricePerCostume;
        if (stat > 150) costumes *= 0.90;

        double total = decor + costumes;
        if (total > budget) {
            System.out.println("Not enough money!");
            System.out.printf("Wingard needs %.2f leva more.%n", total - budget);
        } else {
            System.out.println("Action!");
            System.out.printf("Wingard starts filming with %.2f leva left.%n", budget - total);
        }
    }
}
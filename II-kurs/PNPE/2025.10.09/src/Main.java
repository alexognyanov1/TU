import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);

        BMICalculator calculator = new BMICalculator();
        double bmi = calculator.getBMI(in);
        String status = calculator.getStatus(bmi);
        calculator.ReportResults(0, bmi, status);
    }
}
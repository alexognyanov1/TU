import java.util.Scanner;

public class BMICalculator {
    void printIntroduction() {
        System.out.println("This program calculates your BMI!");
    }

    double getBMI(Scanner in) {
        System.out.println("What is your height in inches?");
        int height = in.nextInt();
        System.out.println("What is your weight in lbs?");
        int weight = in.nextInt();

        return this.bmiFor(height, weight);
    }

    double bmiFor(int height, int weight) {
        double heightCm = height * 2.54;
        double weightKg = weight / 2.205;
        return (weightKg * 703) / (heightCm * heightCm);
    }

    String getStatus(double bmi) {
        if (bmi <= 18.5) {
            return "underweight";
        } else if (bmi <= 25) {
            return "normal";
        } else if (bmi <= 30) {
            return "overweight";
        } else {
            return "obese";
        }
    }

    void ReportResults(int id, double bmi, String status) {
        System.out.printf("Person with id %d has BMI index of %f which is considered %s", id, (Math.round(bmi * 100.0) / 100.0), status);
    }
}

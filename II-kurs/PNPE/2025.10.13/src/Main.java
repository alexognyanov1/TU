import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter task number (1–21): ");
        int choice = sc.nextInt();

        switch (choice) {
            case 1 -> Task01.main(new String[]{});
            case 2 -> Task02.main(new String[]{});
            case 3 -> Task03.main(new String[]{});
            case 4 -> Task04.main(new String[]{});
            case 5 -> Task05.main(new String[]{});
            case 6 -> Task06.main(new String[]{});
            case 7 -> Task07.main(new String[]{});
            case 8 -> Task08.main(new String[]{});
            case 9 -> Task09.main(new String[]{});
            case 10 -> Task10.main(new String[]{});
            case 11 -> Task11.main(new String[]{});
            case 12 -> Task12.main(new String[]{});
            case 13 -> Task13.main(new String[]{});
            case 14 -> Task14.main(new String[]{});
            case 15 -> Task15.main(new String[]{});
            case 16 -> Task16.main(new String[]{});
            case 17 -> Task17.main(new String[]{});
            case 18 -> Task18.main(new String[]{});
            case 19 -> Task19.main(new String[]{});
            case 20 -> Task20.main(new String[]{});
            default -> System.out.println("Invalid task number!");
        }
    }
}

import java.util.Arrays;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

public class Task04 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String day = sc.nextLine().trim();
        Set<String> weekdays = new HashSet<>(Arrays.asList(
                "Monday","Tuesday","Wednesday","Thursday","Friday"));
        Set<String> weekends = new HashSet<>(Arrays.asList("Saturday","Sunday"));
        if (weekdays.contains(day)) System.out.println("Working day");
        else if (weekends.contains(day)) System.out.println("Weekend");
        else System.out.println("Error");
    }
}
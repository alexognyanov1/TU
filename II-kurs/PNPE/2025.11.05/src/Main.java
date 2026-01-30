import java.util.Scanner;
import java.util.regex.Pattern;

public class Main {
    public static final String regexString = "^(?:O-O(?:-O)?|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?)$";
    public static Pattern pattern = Pattern.compile(regexString);

    public static final String winRegexString = "[01½]-[01½]";
    public static Pattern winPattern = Pattern.compile(winRegexString);

    public static void main(String[] args) {
        StringBuilder stringBuilder = new StringBuilder();
        Scanner scanner = new Scanner(System.in);

        while(scanner.hasNextLine()) {
            String line = scanner.nextLine();

            if (!isValidMove(line)) {
                if(isWinMove(line)) {
                    System.out.println("Game over!");
                    break;
                } else {
                    System.out.println("Invalid move! Input a valid move.");
                }
            }

            stringBuilder.append(line).append("\n");
        }

        scanner.close();
        System.out.println(stringBuilder);
    }

    private static boolean isValidMove(String line){
        return pattern.matcher(line).matches();
    }

    private static boolean isWinMove(String line){
        return winPattern.matcher(line).matches();
    }
}
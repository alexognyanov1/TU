package Task2;

public class Main {
    public static void main(String[] args) {
        Logger consoleLogger = new ConsoleLogger();
        Logger fileLogger = new FileLogger();

        Application consoleApp = new Application(consoleLogger);
        Application fileApp = new Application(fileLogger);

        consoleApp.logInfo("User signed in");
        fileApp.logInfo();
    }
}

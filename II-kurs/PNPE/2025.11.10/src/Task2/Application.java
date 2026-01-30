package Task2;

public class Application {
    private final Logger logger;

    public Application(Logger logger) {
        this.logger = logger;
    }

    public void logInfo() {
        logInfo("Application info message");
    }

    public void logInfo(String message) {
        logger.log(message);
    }
}

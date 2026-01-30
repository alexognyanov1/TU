public class Main {
    public static void main(String[] args) {
        if (args.length == 0) {
            printUsage();
            return;
        }

        String mode = args[0].trim().toLowerCase();
        switch (mode) {
            case "server" -> ReportServer.main(new String[0]);
            case "client" -> ReportClient.main(new String[0]);
            default -> printUsage();
        }
    }

    private static void printUsage() {
        System.out.println("Usage:");
        System.out.println("  java Main server  # starts the TCP report server");
        System.out.println("  java Main client  # starts the TCP client console");
    }
}

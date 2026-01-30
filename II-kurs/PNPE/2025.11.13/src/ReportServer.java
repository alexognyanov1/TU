import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.file.Path;
import java.nio.file.Paths;

public class ReportServer {
    private final int port;
    private final ReportCommandProcessor processor;

    public ReportServer(int port) {
        this(
                port,
                Paths.get("main.txt"),
                Paths.get("logs.txt")
        );
    }

    public ReportServer(int port, Path reportFile, Path logFile) {
        this.port = port;
        ReportStorage storage = new ReportStorage(reportFile);
        CommandHistory history = new CommandHistory(logFile);
        this.processor = new ReportCommandProcessor(storage, history);
    }

    public void start() throws IOException {
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Report server listening on port " + port);
            while (true) {
                Socket clientSocket = serverSocket.accept();
                Thread handler = new Thread(new ClientHandler(clientSocket, processor));
                handler.setDaemon(true);
                handler.start();
            }
        }
    }

    public static void main(String[] args) {
        int port = EnvConfig.resolvePort();
        ReportServer server = new ReportServer(port);
        try {
            server.start();
        } catch (IOException e) {
            System.err.println("Unable to start server: " + e.getMessage());
        }
    }
}

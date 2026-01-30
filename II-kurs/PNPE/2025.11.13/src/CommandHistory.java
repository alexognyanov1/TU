import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.List;

/**
 * Persists raw commands and exposes the aggregated history view.
 */
public class CommandHistory {
    private final Path logFile;
    private final Object logLock = new Object();

    public CommandHistory(Path logFile) {
        this.logFile = logFile;
    }

    public void logCommand(String command) {
        if (command == null) {
            return;
        }
        synchronized (logLock) {
            try {
                Files.writeString(
                        logFile,
                        command + System.lineSeparator(),
                        StandardCharsets.UTF_8,
                        StandardOpenOption.CREATE,
                        StandardOpenOption.APPEND
                );
            } catch (IOException e) {
                System.err.println("Failed to write to " + logFile.getFileName() + ": " + e.getMessage());
            }
        }
    }

    public String readHistory() {
        synchronized (logLock) {
            if (!Files.exists(logFile)) {
                try {
                    Files.createFile(logFile);
                } catch (IOException e) {
                    throw new RuntimeException("Error creating logs file");
                }
            }
            try {
                List<String> entries = Files.readAllLines(logFile, StandardCharsets.UTF_8);
                if (entries.isEmpty()) {
                    return "No history available.";
                }
                return String.join(";", entries);
            } catch (IOException e) {
                return "Failed to read " + logFile.getFileName() + ": " + e.getMessage();
            }
        }
    }
}

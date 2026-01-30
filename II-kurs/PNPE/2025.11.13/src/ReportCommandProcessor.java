import java.util.Locale;

public class ReportCommandProcessor {
    private final ReportStorage storage;
    private final CommandHistory history;

    public ReportCommandProcessor(ReportStorage storage, CommandHistory history) {
        this.storage = storage;
        this.history = history;
    }

    public String process(String rawCommand) {
        history.logCommand(rawCommand);

        if (rawCommand == null) {
            return "Command not supported";
        }

        String prepared = rawCommand.trim();
        if (prepared.isEmpty()) {
            return "Command not supported";
        }

        String upper = prepared.toUpperCase(Locale.ROOT);
        if ("REPORT".equals(upper)) {
            return storage.readReport();
        }
        if ("END".equals(upper)) {
            return "Connection closed by server.";
        }
        if ("HISTORY".equals(upper)) {
            return history.readHistory();
        }
        if (upper.startsWith("APPEND:")) {
            return handleAppend(prepared);
        }
        if (upper.startsWith("REPLACE:")) {
            return handleReplace(prepared);
        }

        return "Command not supported";
    }

    private String handleAppend(String command) {
        String payload = extractPayload(command);
        if (payload.isEmpty()) {
            return "Append command requires text after the colon.";
        }
        return storage.appendLine(payload);
    }

    private String handleReplace(String command) {
        String payload = extractPayload(command);
        if (payload.isEmpty()) {
            return "Replace command requires \"replace: <oldWord> <newWord>\" format.";
        }

        String[] parts = payload.split("\\s+", 2);
        if (parts.length < 2) {
            return "Replace command requires two words after the colon.";
        }

        return storage.replaceWord(parts[0], parts[1]);
    }

    private String extractPayload(String command) {
        int colonIndex = command.indexOf(':');
        if (colonIndex == -1 || colonIndex == command.length() - 1) {
            return "";
        }
        return command.substring(colonIndex + 1).trim();
    }
}

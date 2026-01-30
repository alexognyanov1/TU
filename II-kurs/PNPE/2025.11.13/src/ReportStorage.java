import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class ReportStorage {
    private final Path reportFile;
    private final Object reportLock = new Object();

    public ReportStorage(Path reportFile) {
        this.reportFile = reportFile;
    }

    public String readReport() {
        synchronized (reportLock) {
            if (!Files.exists(reportFile)) {
                try {
                    Files.createFile(reportFile);
                    return "";
                } catch (IOException e) {
                    return "Failed to create " + reportFile.getFileName() + ": " + e.getMessage();
                }
            }
            try {
                return Files.readString(reportFile, StandardCharsets.UTF_8);
            } catch (IOException e) {
                return "Failed to read " + reportFile.getFileName() + ": " + e.getMessage();
            }
        }
    }

    public String appendLine(String payload) {
        synchronized (reportLock) {
            try {
                Files.writeString(
                        reportFile,
                        payload + System.lineSeparator(),
                        StandardCharsets.UTF_8,
                        StandardOpenOption.CREATE,
                        StandardOpenOption.APPEND
                );
                return "Text appended to " + reportFile.getFileName() + ".";
            } catch (IOException e) {
                return "Failed to append: " + e.getMessage();
            }
        }
    }

    public String replaceWord(String oldWord, String newWord) {
        synchronized (reportLock) {
            String currentContent;
            try {
                if (!Files.exists(reportFile)) {
                    return reportFile.getFileName() + " is missing.";
                }
                currentContent = Files.readString(reportFile, StandardCharsets.UTF_8);
            } catch (IOException e) {
                return "Failed to read " + reportFile.getFileName() + ": " + e.getMessage();
            }

            if (currentContent.isEmpty()) {
                return reportFile.getFileName() + " is empty. Nothing to replace.";
            }

            int occurrences = countOccurrences(currentContent, oldWord);
            if (occurrences == 0) {
                return "No occurrences of \"" + oldWord + "\" found.";
            }

            String updatedContent = currentContent.replaceAll(oldWord, newWord);
            try {
                Files.writeString(
                        reportFile,
                        updatedContent,
                        StandardCharsets.UTF_8,
                        StandardOpenOption.TRUNCATE_EXISTING,
                        StandardOpenOption.CREATE
                );
            } catch (IOException e) {
                return "Failed to update " + reportFile.getFileName() + ": " + e.getMessage();
            }

            return "Replaced " + occurrences + " occurrence(s) of \"" + oldWord + "\".";
        }
    }

    private int countOccurrences(String content, String target) {
        if (target.isEmpty()) {
            return 0;
        }
        int count = 0;
        int index = 0;
        while ((index = content.indexOf(target, index)) != -1) {
            count++;
            index += target.length();
        }
        return count;
    }
}

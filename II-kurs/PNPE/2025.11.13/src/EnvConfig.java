import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

/**
 * Minimal .env loader (KEY=VALUE lines) so both client and server share one config source.
 */
public final class EnvConfig {
    private static final String DEFAULT_PORT_KEY = "PORT";
    private static final int DEFAULT_PORT = 5000;

    private EnvConfig() {
    }

    public static int resolvePort() {
        return resolvePort(DEFAULT_PORT_KEY, DEFAULT_PORT);
    }

    public static int resolvePort(String key, int fallback) {
        Map<String, String> entries = loadEnvEntries();
        String rawValue = entries.get(key);
        if (rawValue == null || rawValue.isEmpty()) {
            return fallback;
        }
        try {
            return Integer.parseInt(rawValue.trim());
        } catch (NumberFormatException ex) {
            System.err.println("Invalid port \"" + rawValue + "\" in .env, using fallback " + fallback);
            return fallback;
        }
    }

    private static Map<String, String> loadEnvEntries() {
        Map<String, String> entries = new HashMap<>();
        Path envPath = Paths.get(".env");
        if (!Files.exists(envPath)) {
            return entries;
        }

        try (BufferedReader reader = Files.newBufferedReader(envPath, StandardCharsets.UTF_8)) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) {
                    continue;
                }

                int separatorIndex = line.indexOf('=');
                if (separatorIndex <= 0) {
                    continue;
                }

                String key = line.substring(0, separatorIndex).trim();
                String value = line.substring(separatorIndex + 1).trim();
                if (!key.isEmpty()) {
                    entries.put(key, value);
                }
            }
        } catch (IOException e) {
            System.err.println("Failed to load .env: " + e.getMessage());
        }

        return entries;
    }
}

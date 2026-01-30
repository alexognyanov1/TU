import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class ReportClient {
    public static void main(String[] args) {
        int port = EnvConfig.resolvePort();
        try (Socket socket = new Socket("localhost", port);
             DataInputStream input = new DataInputStream(socket.getInputStream());
             DataOutputStream output = new DataOutputStream(socket.getOutputStream());
             BufferedReader console = new BufferedReader(new InputStreamReader(System.in))) {

            System.out.println("Connected to localhost:" + port + ".");
            System.out.println("Available commands: REPORT, APPEND: <text>, REPLACE: <oldWord> <newWord>, HISTORY, END.");

            while (true) {
                System.out.print("> ");
                String command = console.readLine();
                if (command == null) {
                    break;
                }

                command = command.trim();
                if (command.isEmpty()) {
                    continue;
                }

                output.writeUTF(command);
                output.flush();

                String response;
                try {
                    response = input.readUTF();
                } catch (IOException e) {
                    System.out.println("Server disconnected: " + e.getMessage());
                    break;
                }

                System.out.println(response);
                if ("END".equalsIgnoreCase(command)) {
                    break;
                }
            }
        } catch (IOException e) {
            System.err.println("Unable to reach server on port " + port + ": " + e.getMessage());
        }
    }
}

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.EOFException;
import java.io.IOException;
import java.net.Socket;

/**
 * Handles a single TCP client connection and delegates command handling.
 */
public class ClientHandler implements Runnable {
    private final Socket socket;
    private final ReportCommandProcessor processor;

    public ClientHandler(Socket socket, ReportCommandProcessor processor) {
        this.socket = socket;
        this.processor = processor;
    }

    @Override
    public void run() {
        String remoteAddress = socket.getRemoteSocketAddress().toString();
        System.out.println("Client connected: " + remoteAddress);
        try (Socket client = socket;
             DataInputStream input = new DataInputStream(client.getInputStream());
             DataOutputStream output = new DataOutputStream(client.getOutputStream())) {

            boolean running = true;
            while (running) {
                String rawCommand;
                try {
                    rawCommand = input.readUTF();
                } catch (EOFException eof) {
                    break; // client closed connection without END
                }

                if (rawCommand == null) {
                    break;
                }

                String response = processor.process(rawCommand);
                output.writeUTF(response);

                if ("Connection closed by server.".equals(response)) {
                    running = false;
                }

                output.flush();
            }
        } catch (IOException e) {
            System.err.println("Connection error (" + remoteAddress + "): " + e.getMessage());
        } finally {
            System.out.println("Client disconnected: " + remoteAddress);
        }
    }
}

package Task4;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class BookListSerializer {
    public void serialize(List<Book> books, Path destination) {
        try (ObjectOutputStream stream = new ObjectOutputStream(Files.newOutputStream(destination))) {
            stream.writeObject(books);
        } catch (IOException exception) {
            throw new RuntimeException("Unable to serialize books", exception);
        }
    }

    @SuppressWarnings("unchecked")
    public List<Book> deserialize(Path source) {
        try (ObjectInputStream stream = new ObjectInputStream(Files.newInputStream(source))) {
            return (List<Book>) stream.readObject();
        } catch (IOException | ClassNotFoundException exception) {
            throw new RuntimeException("Unable to deserialize books", exception);
        }
    }
}

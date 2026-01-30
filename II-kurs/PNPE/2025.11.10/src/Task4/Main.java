package Task4;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Book> books = new ArrayList<>();
        books.add(new Book("The Pragmatic Programmer", "Andrew Hunt"));
        books.add(new Book("Clean Code", "Robert C. Martin"));
        books.add(new Book("Design Patterns", "Erich Gamma"));

        BookListSerializer serializer = new BookListSerializer();
        Path filePath = Path.of("src", "Task4", "books.ser");
        serializer.serialize(books, filePath);
        List<Book> restored = serializer.deserialize(filePath);
        restored.forEach(System.out::println);
    }
}

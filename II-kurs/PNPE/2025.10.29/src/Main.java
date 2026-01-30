public class Main {
    public static void main(String[] args) {
        try {
            new Student(null, "1234567890");
            new Student("alice", "1234567890");
            new Student("Alice", null);
            new Student("Alice", "1234");
        } catch (StudentNameNullException e) {
            System.out.println("Caught StudentNameNullException: " + e.getMessage());
        } catch (StudentNameCapitalizationException | FacultyNumberNullException | FacultyNumberLengthException e) {
            e.printStackTrace();
        }

        try {
            new ForeignStudent("Maria", "0123456789", null);
            new ForeignStudent("Maria", "0123456789", "spain");
        } catch (CountryNullException e) {
            System.out.println("Caught CountryNullException: " + e.getMessage());
        } catch (CountryCapitalizationException e) {
            System.out.println("Caught CountryCapitalizationException: " + e.getMessage());
        } catch (FacultyNumberNullException | FacultyNumberLengthException | StudentNameCapitalizationException |
                 StudentNameNullException e) {
            e.printStackTrace();
        }
    }
}

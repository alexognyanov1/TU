public class Student {
    private final String name;
    private final String facultyNumber;

    public Student(String name, String facultyNumber) throws StudentNameNullException, StudentNameCapitalizationException, FacultyNumberNullException, FacultyNumberLengthException {
        if (name == null) {
            throw new StudentNameNullException("Student name cannot be null.");
        }
        if (name.isEmpty() || Character.isLowerCase(name.charAt(0))) {
            throw new StudentNameCapitalizationException("Student name must start with an uppercase letter.");
        }
        if (facultyNumber == null) {
            throw new FacultyNumberNullException("Faculty number cannot be null.");
        }
        if (facultyNumber.length() != 10) {
            throw new FacultyNumberLengthException("Faculty number must contain exactly 10 characters.");
        }
        this.name = name;
        this.facultyNumber = facultyNumber;
    }

    public String getName() {
        return name;
    }

    public String getFacultyNumber() {
        return facultyNumber;
    }
}

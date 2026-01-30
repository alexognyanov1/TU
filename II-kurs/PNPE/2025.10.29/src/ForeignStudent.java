public class ForeignStudent extends Student {
    private final String country;

    public ForeignStudent(String name, String facultyNumber, String country) throws CountryNullException, CountryCapitalizationException, StudentNameCapitalizationException, FacultyNumberNullException, FacultyNumberLengthException, StudentNameNullException {
        super(name, facultyNumber);
        if (country == null) {
            throw new CountryNullException("Country cannot be null.");
        }
        if (country.isEmpty() || Character.isLowerCase(country.charAt(0))) {
            throw new CountryCapitalizationException("Country must start with an uppercase letter.");
        }
        this.country = country;
    }

    public String getCountry() {
        return country;
    }
}

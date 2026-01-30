package Task3;

public class CreditCard extends PaymentMethod {
    private final String holderName;
    private final String maskedNumber;

    public CreditCard(String holderName, String maskedNumber) {
        this.holderName = holderName;
        this.maskedNumber = maskedNumber;
    }

    @Override
    public String processPayment(double amount) {
        return String.format("Processed %.2f via credit card for %s (%s)", amount, holderName, maskedNumber);
    }
}

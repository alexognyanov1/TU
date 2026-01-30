package Task3;

public class PayPal extends PaymentMethod {
    private final String accountEmail;

    public PayPal(String accountEmail) {
        this.accountEmail = accountEmail;
    }

    @Override
    public String processPayment(double amount) {
        return String.format("Processed %.2f via PayPal for %s", amount, accountEmail);
    }
}

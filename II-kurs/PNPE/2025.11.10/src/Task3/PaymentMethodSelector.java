package Task3;

public class PaymentMethodSelector {
    private final PaymentMethod creditCard;
    private final PaymentMethod payPal;

    public PaymentMethodSelector(PaymentMethod creditCard, PaymentMethod payPal) {
        this.creditCard = creditCard;
        this.payPal = payPal;
    }

    public PaymentMethod select(String methodName) {
        if ("credit".equalsIgnoreCase(methodName) || "card".equalsIgnoreCase(methodName)) {
            return creditCard;
        }
        if ("paypal".equalsIgnoreCase(methodName)) {
            return payPal;
        }
        throw new IllegalArgumentException("Unsupported payment method: " + methodName);
    }
}

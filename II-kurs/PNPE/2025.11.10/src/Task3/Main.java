package Task3;

public class Main {
    public static void main(String[] args) {
        CreditCard creditCard = new CreditCard("Alice Carter", "**** 4590");
        PayPal payPal = new PayPal("alice.carter@example.com");
        PaymentMethodSelector selector = new PaymentMethodSelector(creditCard, payPal);

        double primaryAmount = 125.75;
        String preferredMethod = "credit";
        PaymentMethod chosenMethod = selector.select(preferredMethod);
        System.out.println(chosenMethod.processPayment(primaryAmount));

        double secondaryAmount = 59.30;
        PaymentMethod secondaryMethod = selector.select("paypal");
        System.out.println(secondaryMethod.processPayment(secondaryAmount));
    }
}

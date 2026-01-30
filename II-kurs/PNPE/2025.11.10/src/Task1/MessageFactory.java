package Task1;

import java.util.Locale;

class MessageFactory {
    static Message createMessage(String type) {
        if (type == null) {
            throw new IllegalArgumentException("Task1.Message type cannot be null");
        }
        String normalized = type.toLowerCase(Locale.ROOT).trim();
        return switch (normalized) {
            case "email" -> new EmailMessage();
            case "sms" -> new SMSMessage();
            case "push" -> new PushNotification();
            default -> throw new IllegalArgumentException("Unsupported message type: " + type);
        };
    }
}

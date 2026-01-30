package Task1;

class PushNotification implements Message {
    @Override
    public void send() {
        System.out.println("Push notification sent");
    }
}

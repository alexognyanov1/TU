package Task1;

class SMSMessage implements Message {
    @Override
    public void send() {
        System.out.println("SMS message sent");
    }
}

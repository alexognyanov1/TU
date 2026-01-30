package Task1;

class EmailMessage implements Message {
    @Override
    public void send() {
        System.out.println("Email message sent");
    }
}

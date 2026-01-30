package Task2;

public class Lamp implements Switchable, Describable {
    private boolean status;

    public void turnOn() {
        status = true;
        System.out.println("Lamp is turned on");
    }

    public void turnOff() {
        status = false;
        System.out.println("Lamp is turned off");
    }

    public boolean isOn() {
        return status;
    }

    public void describe() {
        System.out.println("This is a desk lamp");
    }
}

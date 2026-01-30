package Task2;

public class TV implements Switchable, Describable {
    private boolean status = false;

    public void turnOn() {
        status = true;
        System.out.println("TV is turned on");
    }

    public void turnOff() {
        status = false;
        System.out.println("TV is turned off");
    }

    public boolean isOn() {
        return status;
    }

    public void describe() {
        System.out.println("This is a smart TV");
    }
}


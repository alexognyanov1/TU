package Task1;

public abstract class Shape {
    private final String color;

    public Shape(String _color) {
        color = _color;
    }

    public abstract double area();

    public abstract double perimeter();

    public void displayColor() {
        System.out.println("Color of the shape is: " + color);
    }
}

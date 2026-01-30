package Task1;

public class Circle extends Shape {
    private final double radius;

    public Circle(double _radius, String _color) {
        super(_color);
        radius = _radius;
    }

    public double area() {
        return Math.PI * (radius * radius);
    }

    public double perimeter() {
        return Math.PI * 2 * radius;
    }
}

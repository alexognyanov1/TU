package Task1;

public class Rectangle extends Shape {
    private final double width;
    private final double height;

    public Rectangle(double _width, double _height, String _color) {
        super(_color);
        width = _width;
        height = _height;
    }

    public double area() {
        return width * height;
    }

    public double perimeter() {
        return (width + height) * 2;
    }
}

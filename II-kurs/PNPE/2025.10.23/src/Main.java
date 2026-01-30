import Task1.Circle;
import Task1.Rectangle;
import Task1.Shape;
import Task2.Lamp;
import Task2.Switchable;
import Task2.TV;

import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        task2();
    }

    static void task1() {
        Shape circle = new Circle(10, "red");
        Shape rectangle = new Rectangle(10, 15, "black");

        ArrayList<Shape> l = new ArrayList<Shape>();
        l.addLast(circle);
        l.addLast(rectangle);

        for (Shape i : l) {
            if (i instanceof Circle) {
                System.out.println("Circle");
            } else {
                System.out.println("Rectangle");
            }
            i.displayColor();
            System.out.println(i.area());
            System.out.println(i.perimeter());
        }
    }

    static void task2() {
        Lamp lamp = new Lamp();
        TV tv = new TV();

        ArrayList<Switchable> l = new ArrayList<Switchable>();

        l.addLast(lamp);
        l.addLast(tv);

        for (Switchable i : l) {
            i.turnOn();
        }

        lamp.describe();
        tv.describe();
    }
}
package Task2;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class Car {
    private String brand;
    private String model;
    private String color;
    private int power;
    private String engineType;
    private String transmissionType;
    private int year;

    public Car() {}

    public Car(String brand, String model, String color, int power, String engineType, String transmissionType, int year) {
        this.brand = brand;
        this.model = model;
        this.color = color;
        this.power = power;
        this.engineType = engineType;
        this.transmissionType = transmissionType;
        this.year = year;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public int getPower() {
        return power;
    }

    public void setPower(int power) {
        this.power = power;
    }

    public String getEngineType() {
        return engineType;
    }

    public void setEngineType(String engineType) {
        this.engineType = engineType;
    }

    public String getTransmissionType() {
        return transmissionType;
    }

    public void setTransmissionType(String transmissionType) {
        this.transmissionType = transmissionType;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    public static List<Car> filterByFirstLetter(List<Car> cars, char letter) {
        List<Car> result = new ArrayList<>();
        for (Car car : cars) {
            if (car.getBrand().toLowerCase().charAt(0) == Character.toLowerCase(letter)) {
                result.add(car);
            }
        }
        return result;
    }

    public static List<Car> sortByBrand(List<Car> cars, boolean ascending) {
        List<Car> sorted = new ArrayList<>(cars);
        sorted.sort((a, b) -> ascending ?
                a.getBrand().compareToIgnoreCase(b.getBrand()) :
                b.getBrand().compareToIgnoreCase(a.getBrand()));
        return sorted;
    }

    public static List<Car> removeDuplicates(List<Car> cars) {
        Set<Car> uniqueCars = new LinkedHashSet<>(cars);
        return new ArrayList<>(uniqueCars);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Car other)) return false;
        return brand.equalsIgnoreCase(other.brand) &&
                model.equalsIgnoreCase(other.model) &&
                year == other.year;
    }

    @Override
    public int hashCode() {
        return (brand + model + year).toLowerCase().hashCode();
    }

    @Override
    public String toString() {
        return brand + " " + model + " (" + year + "), " + color + ", " + engineType + ", " + transmissionType + ", " + power + " HP";
    }
}


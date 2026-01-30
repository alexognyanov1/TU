package model;

import java.util.HashSet;

public class Client {
    private int id;
    private final String name;
    private final HashSet<String> services;

    public Client(int _id, String _name) {
        id = _id;
        name = _name;
        services = new HashSet<String>();
    }

    public void addService(String name) {
        services.add(name);
    }

    @Override
    public String toString() {
        return "id: " + id + " " + name + ": " + String.join(",", services) + ";";
    }

    public String getName() {
        return name;
    }

    public int getId() {
        return id;
    }
}

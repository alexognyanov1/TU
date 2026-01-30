package service;

import model.Client;

import java.util.ArrayDeque;
import java.util.LinkedList;

public class BankQueueService {
    private final LinkedList<Client> clients = new LinkedList<Client>();
    private final ArrayDeque<Client> serveClients = new ArrayDeque<Client>();

    public void clientArrived(Client c) {
        clients.addFirst(c);
        serveClients.addFirst(c);
    }

    public Client processNextClient() {
        return serveClients.pollLast();
    }

    public Boolean hasWaitingClients() {
        return serveClients.isEmpty();
    }

    public LinkedList<Client> getArrivalOrder() {
        return clients;
    }
}

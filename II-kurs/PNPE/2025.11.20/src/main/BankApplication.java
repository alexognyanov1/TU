package main;

import model.Client;
import service.BankQueueService;
import service.OperationService;

import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedList;

public class BankApplication {
    public static void main() {
        Client c1 = new Client(5, "Gosho");
        Client c2 = new Client(4, "Gosho1");
        Client c3 = new Client(3, "Gosho2");
        Client c4 = new Client(2, "Gosho3");
        Client c5 = new Client(1, "Gosho4");

        BankQueueService bqs = new BankQueueService();
        OperationService ops = new OperationService();

        bqs.clientArrived(c1);
        bqs.clientArrived(c2);
        bqs.clientArrived(c3);
        bqs.clientArrived(c4);
        bqs.clientArrived(c5);

        ops.provideServices(bqs.processNextClient(), "withdraw");
        ops.provideServices(bqs.processNextClient(), "withdraw");
        ops.provideServices(bqs.processNextClient(), "withdraw");
        ops.provideServices(bqs.processNextClient(), "withdraw");

        Client lastClient = bqs.processNextClient();
        ops.provideServices(lastClient, "deposit");
        ops.provideServices(lastClient, "withdraw");

        ops.undo();

        LinkedList<Client> allClients = bqs.getArrivalOrder();
        System.out.println(allClients);
        allClients.sort(Comparator.comparingInt(Client::getId).reversed());

        System.out.println(allClients);
    }
}

package service;

import model.Client;
import util.OperationLog;

public class OperationService {
    private final OperationLog logger = new OperationLog();

    public void provideServices(Client c, String action) {
        c.addService(action);
        logger.log(c.getName() + " performed: " + action);
    }

    public void undo() {
        System.out.printf("Undo: %s\n", logger.undo());
    }
}

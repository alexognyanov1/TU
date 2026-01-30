package util;

import java.util.ArrayDeque;

public class OperationLog {
    private final ArrayDeque<String> actionLog = new ArrayDeque<String>();

    public void log(String action) {
        actionLog.addLast(action);
    }

    public String undo() {
        return actionLog.removeLast();
    }
}

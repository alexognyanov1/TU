package task5;

import java.util.List;
import java.util.stream.Collectors;

public class TextTransformer {
    public static List<String> applyTransform(List<String> input, StringTransformer transformer) {
        return input.stream()
                .map(transformer::transform)
                .collect(Collectors.toList());
    }
}

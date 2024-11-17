import lombok.Data;

import java.util.Map;

@Data
public class Movie {
    private String description;
    private Map<String, Double> features;
    private Integer rating;

    public Movie() {
    }

    public Movie(String description, Map<String, Double> features) {
        this.description = description;
        this.features = features;
    }
}

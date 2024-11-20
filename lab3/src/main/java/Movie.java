import lombok.Data;
import java.util.Map;

/**
 * Klasa reprezentuje film zawierający opis, zestaw cech oraz opcjonalną ocenę.
 *
 * Pola:
 * - description - krótki opis filmu.
 * - features - mapa cech filmu, gdzie kluczami są nazwy cech, a wartościami ich wagi.
 * - rating - opcjonalna ocena filmu w formie liczby całkowitej.
 */
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

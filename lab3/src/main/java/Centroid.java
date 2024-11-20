import lombok.Data;
import java.util.Map;
/**
 * Reprezentuje centroid z określonymi współrzędnymi w przestrzeni cech.
 *
 * Pola:
 * - coordinates - mapa współrzędnych centroidu, gdzie kluczami są nazwy cech,
 *   a wartościami są odpowiadające im wagi (wartości liczbowe).
 */
@Data
public class Centroid {
    private final Map<String, Double> coordinates;

}

package interfaces;
import java.util.Map;
/**
 * Interfejs do obliczania odległości między dwoma zbiorami cech.
 *
 * Metody:
 * - calculate - oblicza odległość między dwoma mapami cech.
 */
public interface Distance {
    /**
     * Oblicza odległość między dwoma zbiorami cech reprezentowanymi jako mapy.
     *
     * @param f1 pierwsza mapa cech, gdzie klucz to nazwa cechy, a wartość to jej waga.
     * @param f2 druga mapa cech, gdzie klucz to nazwa cechy, a wartość to jej waga.
     * @return wartość odległości między dwoma zbiorami cech.
     */
    double calculate(Map<String, Double> f1, Map<String, Double> f2);
}

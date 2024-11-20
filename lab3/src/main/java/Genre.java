import lombok.Data;
/**
 * Reprezentuje gatunek filmowy z nazwą, oceną oraz wartością liczbową.
 *
 * Pola:
 * - name - nazwa gatunku filmowego.
 * - rate - ocena gatunku w formie liczby całkowitej.
 * - value - dodatkowa wartość numeryczna związana z gatunkiem.
 */
@Data
public class Genre {
    private String name;
    private int rate;
    private double value;

    public Genre(String name, int rate, double value) {
        this.name = name;
        this.rate = rate;
        this.value = value;
    }
}

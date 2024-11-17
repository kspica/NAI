import lombok.Data;

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

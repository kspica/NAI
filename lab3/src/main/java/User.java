import lombok.Data;
import java.util.List;
/**
 * Reprezentuje użytkownika z imieniem oraz listą obejrzanych filmów.
 *
 * Pola:
 * - name - imię użytkownika.
 * - movies - lista filmów obejrzanych przez użytkownika.
 */
@Data
public class User {
    private String name;
    private List<Movie> movies;
}

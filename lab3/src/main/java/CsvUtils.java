import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class CsvUtils {
    /**
     * Odczytuje plik i tworzy listę użytkowników wraz z ich ocenionymi filmami.
     *
     * @param file plik zawierający dane użytkowników w formacie: imię i nazwisko;film1;ocena1;film2;ocena2;...
     * @return lista użytkowników, z których każdy zawiera swoje imię i nazwisko oraz listę ocenionych filmów
     */
    public static List<User> getUsersFromFile(File file) {
        List<User> users = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = br.readLine()) != null) {
                User user = new User();
                List<Movie> movies = new ArrayList<>();
                String[] splitedLine = line.split(";");
                user.setName(splitedLine[0]);
                for (int i = 1; i < splitedLine.length; i += 2) {
                    Movie movie = new Movie();
                    movie.setDescription(splitedLine[i]);
                    movie.setRating(Integer.valueOf(splitedLine[i + 1]));
                    movies.add(movie);
                }
                user.setMovies(movies);
                users.add(user);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        return users;
    }
    /**
     * Odczytuje plik i tworzy listę filmów ocenionych przez użytkowników.
     *
     * @param file plik zawierający dane filmów w formacie: film;gatunek1;gatunek2;...
     * @return lista filmów, z których każdy zawiera opis oraz przypisane gatunki
     */
    public static List<Movie> getMoviesRatedByUsers(File file) {
        List<Movie> movies = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = br.readLine()) != null) {
                Map<String, Double> geners = new HashMap<>();
                Movie movie = new Movie();
                String[] splitLine = line.split(";");
                movie.setDescription(splitLine[0]);
                for (int i = 1; i < splitLine.length; i++) {
                    geners.put(splitLine[i], 66d);
                }
                movie.setFeatures(geners);
                movies.add(movie);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        return movies;
    }

    /**
     * Odczytuje plik CSV zawierający listę 1000 najlepszych filmów IMDb i wyodrębnia ich szczegóły.
     *
     * @param filePath ścieżka do pliku CSV
     * @return lista filmów z nazwami oraz gatunkami, wraz z losowymi ocenami gatunków
     */
    public static List<Movie> getTop1000MoviesImdb(File filePath) {
        List<Movie> movies = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            Random random = new Random();
            br.readLine();
            while ((line = br.readLine()) != null) {
                List<String> values = parseCsvLine(line);
                Map<String, Double> genres = new HashMap<>();
                String movieName;
                movieName = values.get(1).trim();
                for (String genre : values.get(5).split(",")) {
                    genres.put(genre.trim(), (double) random.nextInt(101));

                }
                movies.add(new Movie(movieName, genres));

            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        return movies;
    }

    /**
     * Parsuje linię z pliku CSV, uwzględniając wartości w cudzysłowach oraz oddzielone przecinkami.
     *
     * @param line pojedyncza linia z pliku CSV
     * @return lista wartości wyodrębnionych z linii
     */
    public static List<String> parseCsvLine(String line) {
        List<String> values = new ArrayList<>();
        Pattern pattern = Pattern.compile("\"([^\"]*)\"|([^,]+)");
        Matcher matcher = pattern.matcher(line);

        while (matcher.find()) {
            if (matcher.group(1) != null) {
                values.add(matcher.group(1));
            } else {
                values.add(matcher.group(2).trim());
            }
        }
        return values;
    }


}
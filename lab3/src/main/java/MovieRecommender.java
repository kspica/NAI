import implementations.EuclideanDistance;

import java.io.File;
import java.util.*;
import java.util.stream.Collectors;

import static java.util.stream.Collectors.toSet;

/**
 * Opis problemu:
 * Silnik rekomendujący filmy na bazie preferencji użytkownika, implementuje on algorytm K-Means który w tym przypadku
 * używa dystans euklidesowy żeby wygenerować klastry które będa zawierały filmy o zbliżonych parametrach. Filmy są opisywane
 * przez mapę zawierającą parę klucz - wartość w której klucz to gatunek a wartość to liczba za zakresu 0 - 100 która mówi nam
 * jak bardzo dany film odpowiada gatunkowi z mapy. Parametr ten jest generowany losowo ze względu na brak dostępu do takich danych.
 * Nastęnie aplikacja pobiera użytkowników wraz z ocenionymi przez nich filmami, sprawdza jakie są ulubione gatunki danego użytkownika
 * i na tej podstawie znajduje centroid najbardziej pasujący do upodobań użytkownika oraz generuje rekomendacje i antyrekomendacje.
 * <p>
 * Wykonawcy:
 * Sebastian Kalwasiński s25535, Karol Spica s15990
 */
public class MovieRecommender {


    /**
     * Główna metoda uruchamiająca rekomendacje filmów dla użytkownika.
     * Wczytuje dane z plików CSV, przetwarza dane o użytkownikach i filmach, a następnie generuje rekomendacje filmów na podstawie ulubionych gatunków użytkownika.
     */
    public static void main(String[] args) {
        File file = new File("src/main/resources/imdbTop1000.csv");
        File usersFile = new File("src/main/resources/usersMovies.csv");
        File moviesRatedByUser = new File("src/main/resources/movieRatedByUsers.csv");
        List<String> recommendedMovies;
        List<String> unrecommendedMovies;
        List<Movie> movies;
        List<User> users;
        List<Movie> moviesRatedByUsers;

        users = CsvUtils.getUsersFromFile(usersFile);
        movies = CsvUtils.getTop1000MoviesImdb(file);
        moviesRatedByUsers = CsvUtils.getMoviesRatedByUsers(moviesRatedByUser);
        Map<Centroid, List<Movie>> clusters = KMeans.fit(movies, 4, new EuclideanDistance(), 1000);

        Scanner scanner = new Scanner(System.in);
        System.out.print("Wpisz imię i nazwisko użytkownika dla którego chcesz otrzymać rekomendację: \n");
        users.forEach(user -> System.out.println(user.getName()));

        String name = scanner.nextLine();
        User user = users.stream()
                .filter(usr -> usr.getName().equals(name))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("Podany użytkownik nie istnieje"));

        List<String> userFavoriteGenresBasedOnRatings = findUserFavoriteGenres(user, moviesRatedByUsers);
        recommendedMovies = findMovieFromGivenCentroid(clusters.get(findBestClusterForUser(clusters, userFavoriteGenresBasedOnRatings)));
        unrecommendedMovies = findMovieFromGivenCentroid(clusters.get(findWorstClusterForUser(clusters, userFavoriteGenresBasedOnRatings)));
        System.out.println("Oto rekomendacje dla Ciebie bazujące na ocenionych przez Ciebie filmach: " + recommendedMovies);
        System.out.println("Oto antyrekomendacje dla Ciebie bazujące na ocenionych przez Ciebie filmach: " + unrecommendedMovies);


        scanner.close();
    }

    /**
     * Znajduje ulubione gatunki użytkownika na podstawie ocenionych przez niego filmów.
     *
     * @param user               użytkownik, którego ulubione gatunki mają zostać znalezione
     * @param moviesRatedByUsers lista filmów ocenionych przez użytkowników
     * @return lista ulubionych gatunków użytkownika
     */
    private static List<String> findUserFavoriteGenres(User user, List<Movie> moviesRatedByUsers) {
        List<Genre> genresRating = new ArrayList<>();
        List<String> favoriteGenres;
        for (Movie movie : user.getMovies()) {
            Movie movieWithGenres = moviesRatedByUsers.stream()
                    .filter(mov -> mov.getDescription().equals(movie.getDescription()))
                    .findFirst()
                    .orElse(null);
            if (movieWithGenres != null) {
                movieWithGenres.setRating(movie.getRating());
                genresRating.addAll(movieWithGenres.getFeatures().entrySet()
                        .stream()
                        .map(e -> new Genre(e.getKey(), movieWithGenres.getRating(), e.getValue()))
                        .collect(Collectors.toList()));
            }
        }
        favoriteGenres = computeFavoriteGenres(genresRating);

        return favoriteGenres;
    }

    /**
     * Oblicza ulubione gatunki użytkownika na podstawie ocen filmów.
     *
     * @param genersRating lista gatunków z ocenami
     * @return lista ulubionych gatunków użytkownika posortowanych według wartości średnich
     */
    private static List<String> computeFavoriteGenres(List<Genre> genersRating) {
        Map<String, Double> genresWithAverageValue = new HashMap<>();
        Map<String, List<Genre>> groupedByName = genersRating.stream()
                .collect(Collectors.groupingBy(Genre::getName));

        for (Map.Entry<String, List<Genre>> entry : groupedByName.entrySet()) {
            String name = entry.getKey();
            List<Genre> genreList = entry.getValue();

            double totalValue = genreList.stream().mapToDouble(gener -> (double) gener.getRate() / 10 * gener.getValue()).sum();
            double averageValue = totalValue / genreList.size();

            genresWithAverageValue.put(name, averageValue);
        }
        return genresWithAverageValue.entrySet().stream()
                .sorted((entry1, entry2) -> entry2.getValue().compareTo(entry1.getValue()))
                .limit(3)
                .map(Map.Entry::getKey)
                .collect(Collectors.toList());
    }

    /**
     * Znajduje rekomendowane filmy dla użytkownika na podstawie najlepszego klastra.
     *
     * @param moviesFromBestCentroidForUser lista filmów z najlepszego klastra użytkownika
     * @return lista rekomendowanych filmów
     */
    private static List<String> findMovieFromGivenCentroid(List<Movie> moviesFromBestCentroidForUser) {
        return getRandomItems(moviesFromBestCentroidForUser, 5)
                .stream()
                .map(Movie::getDescription)
                .collect(Collectors.toList());
    }

    /**
     * Wybiera losowe elementy z listy.
     *
     * @param list          lista elementów
     * @param numberOfItems liczba elementów do wybrania
     * @param <T>           typ elementów w liście
     * @return lista losowo wybranych elementów
     */
    private static <T> List<T> getRandomItems(List<T> list, int numberOfItems) {
        if (list.size() < numberOfItems) {
            throw new IllegalArgumentException("Lista ma za mało elementów.");
        }

        List<T> copy = new ArrayList<>(list);
        Collections.shuffle(copy);
        return copy.subList(0, numberOfItems);
    }

    /**
     * Znajduje najlepszy klaster dla użytkownika na podstawie gatunków, które lubi.
     *
     * @param clusters   mapa centrów (klastrów) i przypisanych do nich filmów
     * @param userGenres lista gatunków preferowanych przez użytkownika
     * @return centroid najlepszego klastra
     */
    private static Centroid findBestClusterForUser(Map<Centroid, List<Movie>> clusters, List<String> userGenres) {
        double bestScore = 0.0;
        Centroid bestCentroid = null;
        for (Map.Entry<Centroid, List<Movie>> entry : clusters.entrySet()) {
            Double score = 0.0;
            for (String genre : userGenres) {
                score += entry.getKey().getCoordinates().get(genre);
                if (bestScore < score) {
                    bestScore = score;
                    bestCentroid = entry.getKey();
                }
            }
        }

        return bestCentroid;
    }

    /**
     * Znajduje najgorszy klaster dla użytkownika na podstawie gatunków, które lubi.
     *
     * @param clusters   mapa centrów (klastrów) i przypisanych do nich filmów
     * @param userGenres lista gatunków preferowanych przez użytkownika
     * @return centroid najgorszego klastra
     */
    private static Centroid findWorstClusterForUser(Map<Centroid, List<Movie>> clusters, List<String> userGenres) {
        double worstScore = 100.0;
        Centroid worstCentroid = null;
        for (Map.Entry<Centroid, List<Movie>> entry : clusters.entrySet()) {
            Double score = 0.0;
            for (String genre : userGenres) {
                score += entry.getKey().getCoordinates().get(genre);
                if (worstScore > score) {
                    worstScore = score;
                    worstCentroid = entry.getKey();
                }
            }
        }

        return worstCentroid;
    }
}
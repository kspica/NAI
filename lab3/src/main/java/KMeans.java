import interfaces.Distance;

import java.util.*;
import java.util.stream.Collectors;

import static java.util.stream.Collectors.toList;

public class KMeans {
    private static final Random random = new Random();

    /**
     * Przeprowadza algorytm K-means do klasteryzacji zbioru filmów.
     *
     * @param movies lista filmów do klasteryzacji
     * @param k liczba klastrów
     * @param distance obiekt służący do obliczania odległości między punktami
     * @param maxIterations maksymalna liczba iteracji
     * @return mapa, gdzie kluczem jest centroid, a wartością lista filmów przypisanych do tego centroidu
     */

    public static Map<Centroid, List<Movie>> fit(List<Movie> movies, int k, Distance distance, int maxIterations) {
        List<Centroid> centroids = randomCentroids(movies, k);
        Map<Centroid, List<Movie>> clusters = new HashMap<>();
        Map<Centroid, List<Movie>> lastState = new HashMap<>();

        for (int i = 0; i < maxIterations; i++) {
            boolean isLastIteration = i == maxIterations - 1;

            for (Movie movie : movies) {
                Centroid centroid = nearestCentroid(movie, centroids, distance);
                assignToCluster(clusters, movie, centroid);

            }

            boolean shouldTerminate = isLastIteration || clusters.equals(lastState);
            lastState = clusters;
            if (shouldTerminate) {
                break;
            }

            centroids = relocateCentroids(clusters);
            clusters = new HashMap<>();
        }

        return lastState;
    }

    /**
     * Znajduje najbliższy centroid do podanego filmu.
     *
     * @param movie film, do którego szukamy najbliższego centroidu
     * @param centroids lista centroidów
     * @param distance obiekt do obliczania odległości
     * @return najbliższy centroid
     */
    private static Centroid nearestCentroid(Movie movie, List<Centroid> centroids, Distance distance) {
        double minimumDistance = Double.MAX_VALUE;
        Centroid nearest = null;

        for (Centroid centroid : centroids) {
            double currentDistance = distance.calculate(movie.getFeatures(), centroid.getCoordinates());

            if (currentDistance < minimumDistance) {
                minimumDistance = currentDistance;
                nearest = centroid;
            }
        }
        return nearest;
    }

    /**
     * Przypisuje film do odpowiedniego klastra.
     *
     * @param clusters mapa klastrów
     * @param movie film do przypisania
     * @param centroid centroid, do którego przypisujemy film
     */
    private static void assignToCluster(Map<Centroid, List<Movie>> clusters, Movie movie, Centroid centroid) {
        clusters.compute(centroid, (key, list) -> {
            if (list == null) {
                list = new ArrayList<>();
            }

            list.add(movie);
            return list;
        });
    }

    /**
     * Generuje początkowe centroidy losowo na podstawie cech filmów.
     *
     * @param movies lista filmów
     * @param k liczba centroidów
     * @return lista początkowych centroidów
     */
    private static List<Centroid> randomCentroids(List<Movie> movies, int k) {
        List<Centroid> centroids = new ArrayList<>();
        Map<String, Double> maxs = new HashMap<>();
        Map<String, Double> mins = new HashMap<>();

        for (Movie movie : movies) {
            movie.getFeatures().forEach((key, value) -> {
                maxs.compute(key, (k1, max) -> max == null || value > max ? value : max);
            });
            movie.getFeatures().forEach((key, value) -> {
                mins.compute(key, (k1, min) -> min == null || value < min ? value : min);
            });
        }

        Set<String> attributes = movies.stream()
                .flatMap(e -> e.getFeatures().keySet().stream())
                .collect(Collectors.toSet());

        for (int i = 0; i < k; i++) {
            Map<String, Double> coordinates = new HashMap<>();
            for (String attribute : attributes) {
                double max = maxs.get(attribute);
                double min = mins.get(attribute);
                coordinates.put(attribute, random.nextDouble() * (max - min) + min);
            }
            centroids.add(new Centroid(coordinates));
        }

        return centroids;
    }

    /**
     * Przemieszcza centroidy do nowych pozycji na podstawie średnich wartości przypisanych filmów.
     *
     * @param clusters mapa klastrów
     * @return lista zaktualizowanych centroidów
     */
    private static List<Centroid> relocateCentroids(Map<Centroid, List<Movie>> clusters) {
        return clusters.entrySet().stream().map(e -> average(e.getKey(), e.getValue())).collect(toList());
    }

    /**
     * Oblicza średnią pozycję centroidu na podstawie filmów przypisanych do tego centroidu.
     *
     * @param centroid centroid, dla którego obliczamy średnią
     * @param movies lista filmów przypisanych do centroidu
     * @return nowy centroid z uśrednionymi współrzędnymi
     */
    private static Centroid average(Centroid centroid, List<Movie> movies) {
        if (movies == null || movies.isEmpty()) {
            return centroid;
        }

        Map<String, Double> average = centroid.getCoordinates();
        movies.stream().flatMap(e -> e.getFeatures().keySet().stream())
                .forEach(k -> average.put(k, 0.0));

        for (Movie movie : movies) {
            movie.getFeatures().forEach((k, v) -> average.compute(k, (k1, currentValue) -> currentValue + v));
        }

        average.forEach((k, v) -> average.put(k, v / movies.size()));

        return new Centroid(average);
    }
}

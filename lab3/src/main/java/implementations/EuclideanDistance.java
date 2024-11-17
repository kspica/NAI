package implementations;

import interfaces.Distance;

import java.util.Map;

public class EuclideanDistance implements Distance {

    /**
     * Oblicza odległość euklidesową pomiędzy dwoma wektorami cech (f1 i f2).
     * Jest to klasyczna miara odległości, stosowana w algorytmie K-means do określenia bliskości punktów (filmów) względem centroidu.
     *
     * @param f1 mapa cech pierwszego obiektu, gdzie kluczem jest nazwa cechy, a wartością jej wartość numeryczna
     * @param f2 mapa cech drugiego obiektu, w takim samym formacie jak f1
     * @return odległość euklidesowa pomiędzy obiektami f1 i f2
     */
    @Override
    public double calculate(Map<String, Double> f1, Map<String, Double> f2) {
        double sum = 0;
        for(String key : f1.keySet()) {
            Double v1 = f1.get(key);
            Double v2 = f2.get(key);

            if(v1 != null && v2 != null) {
                sum += Math.pow(v1 - v2, 2);
            }
        }

        return Math.sqrt(sum);
    }
}

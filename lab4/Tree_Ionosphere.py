import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from utilities import visualize_classifier

"""
Autorzy: Sebastian Kalwasiński, Karol Spica
Biblioteki:
- numpy
- scikit-learn

Opis:
Skrypt implementuje klasyfikację danych z IonosphereDataset.csv za pomocą drzewa decyzyjnego.
Przewiduje klasę dla przykładowych danych wejściowych.
Dane klas dostosowane w zborze danych do potrzeb skryptu. Klasa g oznaczona jako 1, klasa b ozaczona jako 0

Skrypt zawiera dwa podejścia:
1. Klasyfikacja i wizualizacja granicy decyzyjnej z użyciem dwóch wybranych cech (8 i 9).
2. Klasyfikacja z wykorzystaniem wszystkich cech bez wizualizacji.
"""

"""
Ładuje dane z pliku 'IonosphereDataset.csv' i oddziela cechy (X) od etykiet (y).
X: Dane wejściowe.
y: Etykiety klas (0 lub 1).
"""
input_file = 'IonosphereDataset.csv'
data = np.loadtxt(input_file, delimiter=',')
X, y = data[:, :-1], data[:, -1]

"""
Dla wizualizacji ogranicza dane wejściowe do dwóch wybranych cech (kolumny 8 i 9).
"""
X_visual = X[:, [8,9]]

"""
Dzieli dane na zbiory treningowe (75%) i testowe (25%) z ustalonym ziarnem losowości (random_state=5).
Trenuje drzewo decyzyjne na wybranych cechach z głębokością maksymalną równą 8 
"""
X_visual_train, X_visual_test, y_visual_train, y_visual_test = train_test_split(X_visual, y, test_size=0.25, random_state=5)
classifier_visual = DecisionTreeClassifier(random_state=5, max_depth=8)
classifier_visual.fit(X_visual_train, y_visual_train)

"""
Rysuje wykres dla zbioru treningowego i testowego, aby zobaczyć, jak model klasyfikuje punkty.
"""
visualize_classifier(classifier_visual, X_visual_train, y_visual_train, 'Dataset Treningowy z wybranymi cechami do wizualizacji')
visualize_classifier(classifier_visual, X_visual_test, y_visual_test, 'Dataset Testowy z wybranymi cechami do wizualizacj')

"""
Dzieli dane na zbiory treningowe (75%) i testowe (25%) z ustalonym ziarnem losowości (random_state=5).
Trenuje drzewo decyzyjne na wszystkich cechach z głębokością maksymalną równą 8 1
"""
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)
classifier = DecisionTreeClassifier(random_state=5, max_depth=8)
classifier.fit(X_train, y_train)

"""
Autorzy: Sebastian Kalwasiński, Karol Spica

Przewiduje klasy dla zbioru testowego na podstawie wytrenowanego modelu.
Oblicza i wyświetla raport klasyfikacji na podstawie zbioru testowego.
"""
y_test_pred = classifier.predict(X_test)
class_names = ['0', '1']
print("#"*80)
print("Drzewo decyzyjne: Jonosfera\n")
print(classification_report(y_test, y_test_pred, target_names=class_names))
print("#"*80)

"""
Przewiduje klasę dla przykładowych danych wejściowych zawierających wszystkie cechy.
"""
sample_data = [[1,0,0.49870,0.01818,0.43117,-0.09610,0.50649,-0.04156,0.50130,0.09610,0.44675,0.05974,0.55844,
                -0.11948,0.51688,-0.03636,0.52727,-0.05974,0.55325,-0.01039,0.48571,-0.03377,0.49091,-0.01039,
                0.59221,0,0.53215,-0.03280,0.43117,0.03377,0.54545,-0.05455,0.58961,-0.08571]]
predicted_class = classifier.predict(sample_data)
print("Przykładowe dane wejściowe:", sample_data)
print("Wywróżona klasa:", predicted_class)

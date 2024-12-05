import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from utilities import visualize_classifier

"""
Autorzy: Sebastian Kalwasiński, Karol Spica
Biblioteki:
- numpy
- pandas
- scikit-learn

Opis:
Skrypt implementuje klasyfikację danych z PenguinsDataset.csv za pomocą drzewa decyzyjnego.
Przewiduje klasę dla przykładowych danych wejściowych.
Dane klas dostosowane za pomocą enkodera do potrzeb skryptu. Klasa male oznaczona jako 1, klasa female ozaczona jako 0

Skrypt zawiera dwa podejścia:
1. Klasyfikacja i wizualizacja granicy decyzyjnej z użyciem dwóch wybranych cech (2 i 3).
2. Klasyfikacja z wykorzystaniem wszystkich cech bez wizualizacji.
"""

"""
Ładuje dane z pliku 'PenguinsDataset.csv'
"""
input_file = 'PenguinsDataset.csv'
columns = ['species', 'island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm',
           'body_mass_g', 'sex']

data = pd.read_csv(input_file, header=None, names=columns)
# print(data.head())

"""
Tworzy obiekt encoder i koduje etykiety 'sex'
Oddziela cechy (X) od etykiet (y).
X: Dane wejściowe.
y: Etykiety klas (female (0) lub male (1)).
"""
encoder = preprocessing.LabelEncoder()
data['sex'] = encoder.fit_transform(data['sex'])
y = data['sex']
X = data.drop(columns=['sex'])
# print(y.head())

"""
Konwertuje dane z dataframe na tablicę.
Używa tylko cech 2 i 3 dla wizualizacji w dwuwymiarowej przestrzeni.
"""
X = X.values
X_visual = X[:, [2,3]]

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
Trenuje drzewo decyzyjne na wszystkich cechach z głębokością maksymalną równą 8 
"""
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)
classifier = DecisionTreeClassifier(random_state=5, max_depth=8)
classifier.fit(X_train, y_train)

"""
Przewiduje klasy dla zbioru testowego na podstawie wytrenowanego modelu.
Oblicza i wyświetla raport klasyfikacji na podstawie zbioru testowego.
"""
y_test_pred = classifier.predict(X_test)
class_names = ['0', '1']
print("#"*80)
print("Drzewo decyzyjne: Pingwiny\n")
print(classification_report(y_test, y_test_pred, target_names=class_names))
print("#"*80)

"""
Przewiduje klasę dla przykładowych danych wejściowych zawierających wszystkie cechy.
"""
sample_data = [[0,2,32.1,15.5,188,3050]]
predicted_class = classifier.predict(sample_data)
print("Przykładowe dane wejściowe:", sample_data)
if predicted_class == 0:
    print("Wywróżona klasa: female")
elif predicted_class == 1:
    print("Wywróżona klasa: male")

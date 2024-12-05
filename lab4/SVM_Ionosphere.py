import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import svm

"""
Autorzy: Sebastian Kalwasiński, Karol Spica
Biblioteki:
- numpy
- matplotlib
- scikit-learn

Opis:
Skrypt implementuje klasyfikację danych z IonosphereDataset.csv za pomocą maszyny wektorów nośnych (SVM) 
z jądrem RBF. Wizualizuje granicę decyzyjną oraz ocenia skuteczność klasyfikatora na zbiorze testowym.
Przewiduje klasę dla przykładowych danych wejściowych.
Dane klas dostosowane w zborze danych do potrzeb skryptu. Klasa g oznaczona jako 1, klasa b ozaczona jako 0
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
Używa tylko cech 5 i 6 dla wizualizacji w dwuwymiarowej przestrzeni.
"""
X = X[:, [5,6]]

"""
Dzieli dane na zbiory treningowe (75%) i testowe (25%) z ustalonym ziarnem losowości (random_state=5).
"""
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)

"""
Trening klasyfikatora SVM z jądrem RBF.
Parametry: 
- gamma: wpływ pojedyńczych punktów na model, im wyższy tym bardziej lokalny jest wpływ punktu (tworzą się aureole wokoło zamiast większa strefa z punktami)
- c: margines błędu, im wyższa wartość tym węższy margines (z bąbla zrobi się gwiazda byle by tylko złapać wszystkie punkty)
"""
classifier = svm.SVC(kernel='rbf', C=1, gamma=10).fit(X_train, y_train)

"""
Tworzy siatkę punktów w zakresie cech, aby wizualizować granicę decyzyjną.
"""
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
h = (x_max - x_min) / 100

xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

"""
Przewiduje klasy dla punktów w siatce, aby narysować granicę decyzyjną.
"""
Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

"""
Rysuje wykres oraz punkty danych.
"""
plt.figure()
plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8) # Granica decyzyjna
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired, edgecolors='k') # Punkty z danymi
plt.xlabel('Attribute 5')
plt.ylabel('Attribute 6')
plt.title('Jonosfera SVM z jądrem rbf')
plt.show()

"""
Przewiduje klasy dla zbioru testowego na podstawie wytrenowanego modelu.
Oblicza i wyświetla raport klasyfikacji na podstawie zbioru testowego.
"""
y_test_pred = classifier.predict(X_test)
class_names = ['0', '1']
print("#"*80)
print("SVM: Jonosfera\n")
print(classification_report(y_test, y_test_pred, target_names=class_names))
print("#"*80)

"""
Przewiduje klasę dla przykładowych danych wejściowych.
"""
sample_data = [[0.43117,-0.09610]]
predicted_class = classifier.predict(sample_data)
print("Przykładowe dane wejściowe:", sample_data)
print("Wywróżona klasa:", predicted_class)

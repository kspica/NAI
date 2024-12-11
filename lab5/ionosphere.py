import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.src.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

"""
Autorzy: Sebastian Kalwasiński, Karol Spica
Biblioteki:
- os
- numpy
- pandas
- seaborn
- tensorflow
- keras
- matplotlib.pyplot
- scikit-learn

Opis:
Program do klasyfikacji danych jonosfery za pomocą sieci neuronowej.
Dane dostosowane w pliku csv do potrzeb programu. Klasa 0 to bad, 1 to good.

Główne funkcje programu:
- Przygotowanie danych (wczytanie, przetwarzanie, kodowanie etykiet).
- Trenowanie modelu sieci neuronowej lub ładowanie istniejącego modelu.
- Ocena działania modelu na zbiorze testowym, generowanie raportu i wizualizacja wyników.
- Klasyfikacja przykładowych danych wejściowych.
"""

def prepare_data():
    """
    Przygotowuje dane wejściowe do modelu.

    Wczytuje dane z pliku CSV (ionosphere.csv), nadaje odpowiednie nazwy kolumnom,
    rozdziela dane na cechy (x) i etykiety (y) i konwertuje etykiety
    na reprezentację one-hot encoding.

    Zwraca:
        x (ndarray): Dane wejściowe zawierające cechy.
        y (ndarray): Etykiety wyjściowe w postaci zakodowanej (one-hot).
    """

    data = pd.read_csv("datasets/ionosphere.csv")
    data.columns = ([f"Attribute{i}" for i in range(1, 35)] + ["Class"])

    y = data['Class']
    x = data.drop(columns=['Class'])

    y = to_categorical(y, 2)

    return x, y

def get_model(x_train, y_train):
    """
    Tworzy lub ładuje model dla danych Fashion ionosphere.csv.

    Funkcja sprawdza, czy zapisany model istnieje. Jeśli tak, wczytuje model z pliku.
    Jeśli nie, tworzy nowy model, trenuje go na danych treningowych
    i zapisuje do pliku.

    Argumenty:
        x_train (ndarray): Dane treningowe.
        y_train (ndarray): Etykiety treningowe w postaci zakodowanej (one-hot encoding).

    Zwraca:
        model (Sequential): Wytrenowany model sieci neuronowej.
    """

    if os.path.exists("saved_models/ionosphere.keras"):
        model = tf.keras.models.load_model("saved_models/ionosphere.keras")

    else:
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(32, activation='relu', name="Layer_1"),
            tf.keras.layers.Dropout(0.1, name="Dropout_1"),
            tf.keras.layers.Dense(16, activation='relu', name="Layer_2"),
            tf.keras.layers.Dense(2, activation='softmax', name="Output_layer")
        ])

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy'],
        )

        model.fit(x=x_train, y=y_train, epochs=50, batch_size=16, validation_split=0.2)
        model.save("saved_models/ionosphere.keras")

    return model

def print_summary(model, x_test, y_test):
    """
    Wyświetla podsumowanie działania modelu.

    Ocenia model na danych testowych, wyświetla raport klasyfikacji,
    macierz konfuzji oraz przewiduje klasę dla przykładowych danych wejściowych.

    Argumenty:
        model (Sequential): Wytrenowany model sieci neuronowej.
        x_test (ndarray): Dane testowe.
        y_test (ndarray): Etykiety testowe w postaci zakodowanej (one-hot encoding).
    """

    model.evaluate(x_test, y_test)

    y_test_pred = model.predict(x_test, verbose=0)
    y_test_pred = np.argmax(y_test_pred, axis=1)
    y_test = np.argmax(y_test, axis=1)

    class_names = ['bad', 'good']
    print("#" * 80)
    print("Sieci neuronowe: Jonosfera\n")
    print(classification_report(y_test, y_test_pred, target_names=class_names))
    print("#" * 80)

    sample_data = np.array(
        [[1, 0, 0.49870, 0.01818, 0.43117, -0.09610, 0.50649, -0.04156, 0.50130, 0.09610, 0.44675, 0.05974, 0.55844,
          -0.11948, 0.51688, -0.03636, 0.52727, -0.05974, 0.55325, -0.01039, 0.48571, -0.03377, 0.49091, -0.01039,
          0.59221, 0, 0.53215, -0.03280, 0.43117, 0.03377, 0.54545, -0.05455, 0.58961, -0.08571]]) # good

    predicted_class = model.predict(sample_data, verbose=0)
    print("\nPrzykładowe dane wejściowe:\n", sample_data)
    predicted_class_index = np.argmax(predicted_class)
    print("\nWywróżona klasa:", class_names[predicted_class_index])

    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_matrix(y_test, y_test_pred), annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.xlabel('Przewidywane Klasy')
    plt.ylabel('Faktyczne Klasy')
    plt.show()


def main():
    """
    Główna funkcja programu.

    Odpowiada za przygotowanie danych, podział na zbiory treningowy i testowy,
    wytrenowanie modelu oraz wyświetlenie wyników.
    """

    x, y = prepare_data()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=10)

    model = get_model(x_train, y_train)
    print_summary(model, x_test, y_test)

if __name__ == '__main__':
    main()








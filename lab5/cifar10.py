import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.src.datasets import cifar10
from keras.src.utils import to_categorical
from sklearn.metrics import classification_report

"""
Autorzy: Sebastian Kalwasiński, Karol Spica
Biblioteki:
- os
- numpy
- tensorflow
- keras
- matplotlib.pyplot
- scikit-learn

Opis:
Program do klasyfikacji danych CIFAR10 za pomocą sieci neuronowej.
Gotowe dane pobrane z biblioteki keras.

Główne funkcje programu:
- Przygotowanie danych (wczytanie, przetwarzanie, kodowanie etykiet).
- Trenowanie modelu sieci neuronowej lub ładowanie istniejącego modelu.
- Ocena działania modelu na zbiorze testowym, generowanie raportu i wizualizacja wyników.
- Klasyfikacja przykładowego obrazu wejściowego.
"""

def prepare_data():
    """
    Wczytuje dane z gotowego datasetu (CIFAR10) normalizuje je, oraz koduje etykiety (one-hot encoding)

    Zwraca:
        x_train (ndarray): Dane treningowe (obrazy 32x32x3, znormalizowane).
        y_train (ndarray): Etykiety treningowe (one-hot encoding).
        x_test (ndarray): Dane testowe (obrazy 32x32x3, znormalizowane).
        y_test (ndarray): Etykiety testowe (one-hot encoding).
    """

    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)

    return x_train, y_train, x_test, y_test


def get_model1(x_train, y_train):
    """
    Tworzy lub ładuje model1 dla danych CIFAR10.

    Funkcja sprawdza, czy zapisany model istnieje. Jeśli tak, wczytuje model z pliku.
    Jeśli nie, tworzy nowy model, trenuje go na danych treningowych i zapisuje do pliku.

    Argumenty:
        x_train (ndarray): Dane treningowe (obrazy 32x32x3, znormalizowane).
        y_train (ndarray): Etykiety treningowe w postaci zakodowanej (one-hot).

    Zwraca:
        model (Sequential): Wytrenowany model sieci neuronowej.
    """

    if os.path.exists("saved_models/cifar10_1.keras"):
        model = tf.keras.models.load_model("saved_models/cifar10_1.keras")

    else:
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
            tf.keras.layers.Conv2D(16, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        model.fit(x_train, y_train, epochs=15, batch_size=128, validation_split=0.2)
        model.save("saved_models/cifar10_1.keras")

    return model

def get_model2(x_train, y_train):
    """
    Tworzy lub ładuje model2 dla danych CIFAR10.

    Funkcja sprawdza, czy zapisany model istnieje. Jeśli tak, wczytuje model z pliku.
    Jeśli nie, tworzy nowy model, trenuje go na danych treningowych i zapisuje do pliku.

    Argumenty:
        x_train (ndarray): Dane treningowe (obrazy 32x32x3, znormalizowane).
        y_train (ndarray): Etykiety treningowe w postaci zakodowanej (one-hot).

    Zwraca:
        model (Sequential): Wytrenowany model sieci neuronowej.
    """

    if os.path.exists("saved_models/cifar10_2.keras"):
        model = tf.keras.models.load_model("saved_models/cifar10_2.keras")

    else:
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        model.fit(x_train, y_train, epochs=15, batch_size=64, validation_split=0.2)
        model.save("saved_models/cifar10_2.keras")

    return model

def print_summary(model, x_test, y_test):
    """
    Wyświetla podsumowanie działania modelu.

    Ocenia model na danych testowych, wyświetla raport klasyfikacji
    oraz przewiduje klasę dla wybranego przykładu i go wizualizuje.

    Argumenty:
        model (Sequential): Wytrenowany model sieci neuronowej.
        x_test (ndarray): Dane testowe (obrazy 32x32x3, znormalizowane).
        y_test (ndarray): Etykiety testowe w postaci zakodowanej (one-hot encoding).
    """

    model.evaluate(x_test, y_test)

    y_test_pred = model.predict(x_test, verbose=0)
    y_test_pred = np.argmax(y_test_pred, axis=1)
    y_test = np.argmax(y_test, axis=1)

    class_names = ['Airplane', 'Automobile', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']
    print("#" * 80)
    print("Sieci neuronowe: CIFAR-10\n")
    print(classification_report(y_test, y_test_pred, target_names=class_names))
    print("#" * 80)

    sample_data = x_test[1] # Statek
    sample_data = sample_data.reshape(1, 32, 32, 3)
    plt.imshow(x_test[1])
    plt.show()

    predicted_class = model.predict(sample_data)
    predicted_class_index = np.argmax(predicted_class)
    print("Wywróżona klasa:", class_names[predicted_class_index])

def main():
    """
    Główna funkcja programu.

    Odpowiada za przygotowanie danych, podział na zbiory treningowy i testowy,
    wytrenowanie modeli oraz wyświetlenie wyników.
    """

    x_train, y_train, x_test, y_test = prepare_data()
    model1, model2 = get_model1(x_train, y_train), get_model2(x_train, y_train)

    print_summary(model1, x_test, y_test)
    print_summary(model2, x_test, y_test)

if __name__ == '__main__':
    main()

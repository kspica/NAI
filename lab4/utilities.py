import numpy as np
import matplotlib.pyplot as plt

def visualize_classifier(classifier, X, y, title=''):
    """
    Funkcja pobrana z NAI_04_demo
    Wizualizuje granicę decyzyjną klasyfikatora i nakłada na wykres punkty treningowe.

    Funkcja generuje wykres 2D, na którym przedstawiona jest granica decyzyjna klasyfikatora
    utworzona na siatce punktów, a także nałożone są dane treningowe z ich rzeczywistymi
    etykietami (klasami).

    Argumenty:
        classifier (object): Wytrenowany klasyfikator, który implementuje metodę `predict` (np. SVM, DecisionTree).
        X (array-like, shape = [n_samples, 2]): 2D tablica z cechami wejściowymi (zakłada się, że mają dokładnie 2 cechy).
        y (array-like, shape = [n_samples]): 1D tablica etykiet odpowiadających próbkom w `X`.
        title (str, opcjonalny): Tytuł wykresu. Domyślnie pusty ciąg znaków.
    """
    # Define the minimum and maximum values for X and Y
    # that will be used in the mesh grid
    min_x, max_x = X[:, 0].min() - 1.0, X[:, 0].max() + 1.0
    min_y, max_y = X[:, 1].min() - 1.0, X[:, 1].max() + 1.0

    # Define the step size to use in plotting the mesh grid
    mesh_step_size = 0.01

    # Define the mesh grid of X and Y values
    x_vals, y_vals = np.meshgrid(np.arange(min_x, max_x, mesh_step_size), np.arange(min_y, max_y, mesh_step_size))

    # Run the classifier on the mesh grid
    output = classifier.predict(np.c_[x_vals.ravel(), y_vals.ravel()])

    # Reshape the output array
    output = output.reshape(x_vals.shape)

    # Create a plot
    plt.figure()

    # Specify the title
    plt.title(title)

    # Choose a color scheme for the plot
    plt.pcolormesh(x_vals, y_vals, output, cmap=plt.cm.gray)

    # Overlay the training points on the plot
    plt.scatter(X[:, 0], X[:, 1], c=y, s=75, edgecolors='black', linewidth=1, cmap=plt.cm.Paired)

    # Specify the boundaries of the plot
    plt.xlim(x_vals.min(), x_vals.max())
    plt.ylim(y_vals.min(), y_vals.max())

    # Specify the ticks on the X and Y axes
    plt.xticks((np.arange(int(X[:, 0].min() - 1), int(X[:, 0].max() + 1), 1.0)))
    plt.yticks((np.arange(int(X[:, 1].min() - 1), int(X[:, 1].max() + 1), 1.0)))

    plt.show()

"""
- Zasady gry: https://pl.wikipedia.org/wiki/Reversi
- Sebastian Kalwasiński, Karol Spica
- Wymaga do działania biblioteki easyAI - test na wersji 2.0.12
- Ruchy podawanie w formie "wierszkolumna" jako cyfry
- Gramy czarnymi(tym tutaj: ○ ), zaczynami jako pierwsi
"""

from easyAI import TwoPlayerGame, AI_Player, Human_Player, Negamax

class Reversi(TwoPlayerGame):
    def __init__(self, players):
        """
        Inicjalizuje grę Reversi, ustawiając planszę, graczy i podstawowe zmienne.

        Parameters:
        players (List[Player]): Lista graczy biorących udział w grze. Gracze mogą być obiektami klasy CustomHumanPlayer lub AI_Player.

        Attributes:
        self.players (List[Player]): Lista obiektów graczy.
        self.board_size (int): Rozmiar planszy, domyślnie 8x8.
        self.board (List[List[int]]): Aktualny stan planszy, reprezentowany jako lista list liczb.
                                      Zera oznaczają puste pola, jedynki pionki gracza 1, a dwójki pionki gracza 2.
        self.current_player (int): Aktualny gracz, 1 oznacza gracza czarnego, który zaczyna.
        self.directions (List[Tuple[int, int]]): Lista kierunków (x, y), które są używane do sprawdzania poprawności ruchów.
        """

        self.players = players
        self.board_size = 8
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.board[3][3], self.board[4][4] = 2, 2
        self.board[3][4], self.board[4][3] = 1, 1
        self.current_player = 1
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

    def possible_moves(self):
        """
        Zwraca listę wszystkich możliwych ruchów jako współrzędne (x, y).

        Returns:
        List[Tuple[int, int]]: Lista krotek zawierających współrzędne (x, y)
        możliwych ruchów. Każda krotka reprezentuje pole, na którym
        można wykonać ruch.
        """
        
        moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 0 and self.is_valid_move(x, y):
                    moves.append((x, y))
        return moves

    def is_valid_move(self, x, y):
        """
        Sprawdza, czy ruch na pole (x, y) jest możliwy.

        Parameters:
        x (int): Współrzędna x pola, na które ma zostać wykonany ruch.
        y (int): Współrzędna y pola, na które ma zostać wykonany ruch.

        Returns:
        bool: True, jeśli ruch jest możliwy do wykonania False w przeciwnym wypadku.
        """
        for dx, dy in self.directions:
            if self.is_direction_valid(x, y, dx, dy):
                return True
        return False

    def is_direction_valid(self, x, y, dx, dy):
        """
        Sprawdza, czy w danym kierunku (dx, dy) można odwrócić pionki przeciwnika.
        Metoda ocenia, czy po wykonaniu ruchu na pole (x, y) w kierunku
        określonym przez (dx, dy) istnieje możliwość przejęcia pionków
        przeciwnika. Ruch jest uznawany za ważny, jeśli w danym kierunku
        znajduje się co najmniej jeden pionek przeciwnika, a następnie
        własny pionek.

        Parameters:
        x (int): Współrzędna x pola, na które ma zostać wykonany ruch.
        y (int): Współrzędna y pola, na które ma zostać wykonany ruch.
        dx (int): Zmiana współrzędnej x (kierunek w poziomie).
        dy (int): Zmiana współrzędnej y (kierunek w pionie).

        Returns:
        bool: True, jeśli istnieje możliwość odwrócenia pionków przeciwnika
        w danym kierunku, False w przeciwnym wypadku.
        """
        i, j = x + dx, y + dy
        has_opponent_piece = False
        while 0 <= i < self.board_size and 0 <= j < self.board_size:
            if self.board[i][j] == 0:
                return False
            if self.board[i][j] == 3 - self.current_player:
                has_opponent_piece = True
            elif self.board[i][j] == self.current_player:
                return has_opponent_piece
            i += dx
            j += dy
        return False

    def make_move(self, move):
        """
        Wykonuje ruch i odwraca pionki.

        Parameters:
        move (Tuple[int, int]): Krotka zawierająca współrzędne (x, y)
        pola, na które ma zostać wykonany ruch.
        """
        x, y = move
        self.board[x][y] = self.current_player

        for dx, dy in self.directions:
            if self.is_direction_valid(x, y, dx, dy):
                self.flip_in_direction(x, y, dx, dy)

    def flip_in_direction(self, x, y, dx, dy):
        """
        Odwraca pionki w danym kierunku (dx, dy).
        Metoda przekształca pionki przeciwnika na pionki bieżącego gracza
        w kierunku określonym przez (dx, dy), zaczynając od pola
        (x, y) i kontynuując, aż napotka pionek własny lub
        wyjdzie poza planszę.

        Parameters:
        x (int): Współrzędna x pola, od którego rozpoczyna się odwracanie.
        y (int): Współrzędna y pola, od którego rozpoczyna się odwracanie.
        dx (int): Zmiana współrzędnej x (kierunek w poziomie).
        dy (int): Zmiana współrzędnej y (kierunek w pionie).
        """
        i, j = x + dx, y + dy
        while self.board[i][j] == 3 - self.current_player:
            self.board[i][j] = self.current_player
            i += dx
            j += dy

    def show(self):
        """
        Wyświetla aktualny stan planszy z numeracją wierszy i kolumn.
        Metoda renderuje planszę gry w formacie tekstowym, pokazując aktualne
        położenie pionków obu graczy oraz oznaczając puste pola.
        Numeracja kolumn i wierszy zaczyna się od 0.

        W reprezentacji:
        - '○' oznacza pionek gracza 1 (czarny).
        - '●' oznacza pionek gracza 2 (biały).
        - '.' oznacza puste pole.
        """

        print("   " + " ".join([str(i) for i in range(self.board_size)]))

        for i, row in enumerate(self.board):
            line = []
            for j, cell in enumerate(row):
                if cell == 1:
                    line.append('○')
                elif cell == 2:
                    line.append('●')
                else:
                    line.append('.')
            print(f"{i}  " + " ".join(line))
        print("\n")

    def is_over(self):
        """
        Sprawdza, czy gra się skończyła (brak ruchów).

        Returns:
        bool: True, jeśli gra się skończyła (brak dostępnych ruchów),
        False w przeciwnym wypadku.
        """
        return len(self.possible_moves()) == 0

    def scoring(self):
        """
        Zwraca różnicę punktów między graczem a przeciwnikiem.

        Returns:
        int: Różnica punktów, gdzie dodatnia wartość oznacza przewagę
        bieżącego gracza, a ujemna wartość oznacza przewagę przeciwnika.
        """
        return sum([row.count(self.current_player) for row in self.board]) - sum(
            [row.count(3 - self.current_player) for row in self.board])


    def get_winner(self):
        """
        Funkcja drukuje wynik końcowy i informuje kto wygrał grę.
        """
        player_1_score = sum(row.count(1) for row in self.board)
        player_2_score = sum(row.count(2) for row in self.board)

        print(f"Player 1 ( ○ ): {player_1_score} pawns")
        print(f"Player 2 ( ● ): {player_2_score} pawns")

        if player_1_score > player_2_score:
            print("Player 1 ( ○ ) wins!")
        elif player_2_score > player_1_score:
            print("Player 2 ( ● ) wins!")
        else:
            print("Tie!")

# Modyfikacja klasy Human_Player, by wygodnie wpisywać ruch
class CustomHumanPlayer(Human_Player):
    def ask_move(self, game):
        """
        Zapytanie gracza o ruch w formacie x y.

        Metoda pobiera od gracza ruch w formacie dwóch cyfr "xy"
        złączonych razem jako jedna cyfra, a następnie konwertuje je na krotkę
        reprezentującą współrzędne na planszy. Proces trwa, aż gracz
        wprowadzi poprawny ruch, który znajduje się wśród możliwych ruchów.

        Parameters:
        game (Game): Obiekt gry, który udostępnia metodę
        `possible_moves()` do weryfikacji, czy ruch jest dozwolony.

        Returns:
        Tuple[int, int]: Krotka zawierająca współrzędne (x, y)
        reprezentujące ruch gracza.
        """
        move = None
        while move not in game.possible_moves():
            try:
                move_str = input("Make your move (rowcolumn): ")
                move = (int(move_str[0]), int(move_str[1]))
                if move not in game.possible_moves():
                    print("Invalid move, try again.")
            except (ValueError, IndexError):
                print("Invalid input format. Please use 'rowcolumn' together as one number.")
        return move


# Definicja sztucznej inteligencji
ai_algo = Negamax(6)

# Rozpoczęcie gry: gracz vs AI
game = Reversi([CustomHumanPlayer(), AI_Player(ai_algo)])
game.play()

# Gdy gra się zakończy, wyświetl wynik końcowy
if game.is_over():
    game.show()
    game.get_winner()

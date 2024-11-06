import pygame
import Options

class LandingPlatform:
    def __init__(self, x, y):
        """
        Inicjalizuje obiekt LandingPlatform z jego pozycją i wymiarami.

        Parameters:
        x (float): Współrzędna x lewego górnego rogu platformy.
        y (float): Współrzędna y lewego górnego rogu platformy.
        """
        self.x = x
        self.y = y
        self.width = Options.LANDING_PLATFORM_WIDTH
        self.height = 10

    def get_center_pos(self):
        """
        Oblicza i zwraca pozycję środka platformy lądowania.

        Returns:
        tuple: (float, float) reprezentujące współrzędne x i y środka platformy.
        """
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2

        return (center_x, center_y)

    def draw(self,screen):
        """
        Rysuje platformę lądowania jako prostokąt na ekranie.

        Parameters:
        screen (pygame.Surface): Powierzchnia ekranu, na której rysowana jest platforma.
        """
        pygame.draw.rect(screen, Options.GREEN, (self.x, self.y, self.width, self.height))
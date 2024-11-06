import pygame
import math
import numpy as np
import Options

class Rocket:
    def __init__(self, x, y):
        """
        Inicjalizuje obiekt Rocket z jego pozycją, prędkością, kątem, paliwem oraz obrazami.

        Parameters:
        x (float): Początkowa współrzędna x rakiety.
        y (float): Początkowa współrzędna y rakiety.
        """
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.angleDegrees = 0
        self.fuel = 1000
        self.width = 30
        self.height = 60
        self.rocketOff = pygame.transform.scale(pygame.image.load('rocketOff.png'),(self.width, self.height))
        self.rocketOn = pygame.transform.scale(pygame.image.load('rocketOn.png'),(self.width, self.height))
        self.thrusting = False
        self.status = "flying"
        self.autopilot = True

    def get_image(self):
        """
        Zwraca aktualny obraz rakiety w zależności od jej stanu napędu.

        Returns:
        pygame.Surface: Obraz rakiety z włączonym lub wyłączonym napędem.
        """
        if self.thrusting:
            return self.rocketOn
        else:
            return self.rocketOff

    def apply_gravity(self):
        """
        Zastosowuje grawitację do pionowej prędkości rakiety, modyfikując vel_y.
        """
        self.vel_y += Options.GRAVITY

    def apply_thrust(self):
        """
        Zastosowuje napęd do prędkości rakiety, jeśli jest dostępne paliwo. Zmniejsza paliwo
        według określonego współczynnika zużycia i dostosowuje składowe prędkości rakiety.
        Ilość paliwa nie została wzięta pod uwagę w fuzzy logic, bo projekt i tak jest dość rozbudowany
        """
        if self.fuel > 0:
            radians = math.radians(self.angleDegrees)
            self.vel_x += Options.THRUST * math.sin(radians)
            self.vel_y -= Options.THRUST * math.cos(radians)

            self.fuel -= Options.FUEL_CONSUMPTION_RATE

    def rotate(self, direction):
        """
        Obraca rakietę w określonym kierunku, jeśli mieści się w granicach maksymalnego kąta obrotu.

        Parameters:
        direction (str): "left" do obrotu w lewo lub "right" do obrotu w prawo.
        """
        if direction == "left":
            if self.angleDegrees > -Options.MAX_ROCKET_ROTATION:
                self.angleDegrees -= Options.ROTATION_SPEED
        elif direction == "right":
            if self.angleDegrees < Options.MAX_ROCKET_ROTATION:
                self.angleDegrees += Options.ROTATION_SPEED

    def update_position(self):
        """
        Aktualizuje pozycję rakiety na podstawie jej bieżącej prędkości.
        """
        self.x += self.vel_x
        self.y += self.vel_y

    def get_center_pos(self):
        """
        Oblicza i zwraca pozycję środka rakiety.

        Returns:
        tuple: (float, float) reprezentujące współrzędne x i y środka rakiety.
        """
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2

        return (center_x, center_y)

    def get_velocity(self):
        """
        Oblicza i zwraca całkowitą prędkość rakiety jako moduł wektora prędkości.

        Returns:
        float: Moduł wektora prędkości rakiety.
        """
        return np.sqrt(self.vel_x ** 2 + self.vel_y ** 2)

    def draw(self, screen):
        """
        Rysuje rakietę na ekranie w jej aktualnej pozycji i orientacji.

        Parameters:
        screen (pygame.Surface): Powierzchnia ekranu, na której rysowana jest rakieta.
        """
        rotated_image = pygame.transform.rotate(self.get_image(), -self.angleDegrees)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)
        self.thrusting = False
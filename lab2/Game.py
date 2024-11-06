import pygame
import Options
import Rocket
import Platform
import FuzzyLogic


"""
Opis problemu:
Uproszczona gra MoonLander. Sterowanie lądownikiem w czasie rzeczywistym z użyciem logiki rozmytej.

Wykonawcy:
Sebastian Kalwasiński s25535, Karol Spica s15990

Wymagane pakiety pythona do odpalenia gry:
- pygame
- numpy
- scikit-fuzzy
- scipy
- packaging
- networkx
"""

def update_status(rocket, platform):
    """
    Sprawdza, czy rakieta wylądowała na platformie, a jeśli tak, ustala wynik lądowania.

    Jeśli rakieta jest nad platformą i spełnia warunki bezpiecznego lądowania, status rakiety
    zostaje zmieniony na "success". W przeciwnym razie, jeśli lądowanie nie spełnia tych warunków,
    status zmienia się na "crash".

    Parameters:
    rocket (Rocket): Obiekt rakiety.
    platform (LandingPlatform): Obiekt platformy lądowania.
    """
    if (platform.x < rocket.x < platform.x + platform.width and
            platform.y < rocket.y + rocket.height // 2 < platform.y + platform.height):

        if abs(rocket.vel_x) <= Options.MAX_SAFE_VELOCITY and abs(rocket.vel_y) <= Options.MAX_SAFE_VELOCITY and abs(
                rocket.angleDegrees) <= Options.MAX_SAFE_ANGLE:
            rocket.status = "success"
            print("SafeLanding")
        else:
            rocket.status = "crash"
            print("Crashed")


def handle_events(rocket):
    """
    Obsługuje zdarzenia w grze, w tym sterowanie rakietą oraz opcje autopilota.

    Odczytuje naciśnięcia klawiszy, umożliwiając obracanie, przyspieszanie rakiety oraz włączanie
    i wyłączanie autopilota. Zdarzenie zamknięcia okna gry ustawia game_running na False.

    Parameters:
    rocket (Rocket): Obiekt rakiety.

    Returns:
    bool: True, jeśli gra powinna nadal działać, False w przeciwnym razie.
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    # Stearing
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if rocket.status == "flying":
            rocket.rotate("left")

    if keys[pygame.K_d]:
        if rocket.status == "flying":
            rocket.rotate("right")

    if keys[pygame.K_w]:
        if rocket.status == "flying":
            rocket.thrusting = True
            rocket.apply_thrust()

    if not keys[pygame.K_w]:
        rocket.thrusting = False

    if keys[pygame.K_e]:
        rocket.autopilot = True

    if keys[pygame.K_r]:
        rocket.autopilot = False

    if keys[pygame.K_q]:
        return False

    return True


def get_distance(rocket, platform):
    """
    Oblicza dystans między środkiem rakiety a środkiem platformy lądowania.

    Parameters:
    rocket (Rocket): Obiekt rakiety.
    platform (LandingPlatform): Obiekt platformy lądowania.

    Returns:
    tuple: (float, float) reprezentujące dystans w osi X i Y między rakietą a platformą.
    """
    rocket_center_x, rocket_center_y = rocket.get_center_pos()
    platform_center_x, platform_center_y = platform.get_center_pos()

    distance_x = platform_center_x - rocket_center_x
    distance_y = platform_center_y - rocket_center_y

    return distance_x, distance_y


def draw_interface(screen, font, rocket, platform):
    """
    Rysuje interfejs wyświetlający stan gry, w tym informacje o paliwie, prędkości,
    odległości do platformy i kącie rakiety.

    Parameters:
    screen (pygame.Surface): Powierzchnia, na której rysowany jest interfejs.
    font (pygame.font.Font): Czcionka do renderowania tekstu.
    rocket (Rocket): Obiekt rakiety.
    platform (LandingPlatform): Obiekt platformy lądowania.
    """

    # Info about game in left corner
    fuel_text = font.render(f"Fuel: {int(rocket.fuel)}", True, Options.WHITE)
    velocity_x_text = font.render(f"Velocity X: {round(rocket.vel_x, 2)}", True, Options.WHITE)
    velocity_y_text = font.render(f"Velocity Y: {round(rocket.vel_y, 2)}", True, Options.WHITE)
    velocity_text = font.render(f"Velocity: {round(rocket.get_velocity(), 2)}", True, Options.WHITE)

    distance_x_text = font.render(f"Distance X: {round(get_distance(rocket, platform)[0], 2)}", True, Options.WHITE)
    distance_y_text = font.render(f"Distance Y: {round(get_distance(rocket, platform)[1], 2)}", True, Options.WHITE)
    angle_text = font.render(f"Angle: {int(rocket.angleDegrees)}", True, Options.WHITE)
    autopilot_text = font.render(f"Autopilot: {bool(rocket.autopilot)}", True, Options.RED)

    # Draw GUI
    screen.blit(fuel_text, (10, 10))
    screen.blit(velocity_x_text, (10, 30))
    screen.blit(velocity_y_text, (10, 50))
    screen.blit(velocity_text, (10, 70))
    screen.blit(distance_x_text, (10, 90))
    screen.blit(distance_y_text, (10, 110))
    screen.blit(angle_text, (10, 130))
    screen.blit(autopilot_text, (10, 150))


def main():
    """
    Główna funkcja gry Moon Lander, która inicjalizuje wszystkie elementy i obsługuje pętlę gry.

    Tworzy ekran, obiekty rakiety i platformy, oraz kontroler logiki rozmytej. W pętli gry
    obsługuje zdarzenia, aktualizuje stan rakiety, rysuje obiekty i interfejs, a także sprawdza
    status lądowania.

    Po zakończeniu gry zamyka Pygame.
    """
    pygame.init()
    screen = pygame.display.set_mode((Options.WIDTH, Options.HEIGHT))
    pygame.display.set_caption("Moon Lander")
    clock = pygame.time.Clock()

    rocket = Rocket.Rocket(250, 500)
    platform = Platform.LandingPlatform((Options.WIDTH - Options.LANDING_PLATFORM_WIDTH)/2, Options.HEIGHT - 100)

    # Setup fuzzy logic controller
    autopilot_ctrl = FuzzyLogic.setup_fuzzy_logic()

    game_running = True

    while game_running:
        screen.fill(Options.BLACK)
        game_running = handle_events(rocket)
        font = pygame.font.SysFont(None, 24)

        # Update rocket
        if rocket.status == "flying":
            rocket.apply_gravity()
            if rocket.autopilot:
                FuzzyLogic.fuzzy_control(rocket, platform, autopilot_ctrl)  # Use fuzzy control logic
            rocket.update_position()
            update_status(rocket, platform)

        elif rocket.status == "success":
            success_text = font.render("Landing Successful!", True, Options.GREEN)
            screen.blit(success_text, (Options.WIDTH / 2 - 60, Options.HEIGHT / 2))

        elif rocket.status == "crash":
            crash_text = font.render("Crashed!", True, Options.RED)
            screen.blit(crash_text, (Options.WIDTH / 2 - 60, Options.HEIGHT / 2))

        rocket.draw(screen)
        platform.draw(screen)
        draw_interface(screen,font, rocket, platform)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
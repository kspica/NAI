import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import Options
import Game


def setup_fuzzy_logic():
    """
    Konfiguruje system sterowania rozmytego dla działania autopilota.
    Metoda definiuje rozmyte zmienne wejściowe (distance_x, distance_y, velocity_x, velocity_y, angle) oraz
    wyjściowe (thrust, rotate), a także funkcje przynależności dla każdej zmiennej. Następnie ustanawia reguły
    dla systemu sterowania rozmytego, które mają na celu kierowanie ciągiem i rotacją rakiety w oparciu o stan wejściowy.

    Returns:
        autopilot_ctrl (ControlSystem): Skonfigurowany system sterowania rozmytego dla autopilota rakiety.
    """
    distance_x = ctrl.Antecedent(np.arange(-600, 601, 1), 'distance_x')
    distance_y = ctrl.Antecedent(np.arange(-30, 601, 1), 'distance_y')
    velocity_x = ctrl.Antecedent(np.arange(-10, 10, 1), 'velocity_x')
    velocity_y = ctrl.Antecedent(np.arange(-10, 10, 1), 'velocity_y')
    angle = ctrl.Antecedent(np.arange(-Options.MAX_ROCKET_ROTATION, Options.MAX_ROCKET_ROTATION + 1, Options.ROTATION_SPEED), 'angle')

    thrust = ctrl.Consequent(np.arange(0, 2, 1), 'thrust')
    rotate = ctrl.Consequent(np.arange(-1, 2, 1), 'rotate')

    # Fuzzy membership functions
    distance_x.automf(3)
    distance_y.automf(3)
    velocity_x.automf(3)
    velocity_y.automf(3)
    angle.automf(3)

    thrust['on'] = fuzz.trimf(thrust.universe, [1, 1, 1])
    thrust['off'] = fuzz.trimf(thrust.universe, [0, 0, 0])

    rotate['left'] = fuzz.trimf(rotate.universe, [-1, -1, 0])
    rotate['zero'] = fuzz.trimf(rotate.universe, [0, 0, 0])
    rotate['right'] = fuzz.trimf(rotate.universe, [0, 1, 1])

    velocity_x['fast_left'] = fuzz.trimf(velocity_x.universe, [-10, -4, -2])
    velocity_x['slow_left'] = fuzz.trimf(velocity_x.universe, [-3, -1, 0])
    velocity_x['zero'] = fuzz.trimf(velocity_x.universe,      [-1, 0, 1])
    velocity_x['slow_right'] = fuzz.trimf(velocity_x.universe, [0, 1, 3])
    velocity_x['fast_right'] = fuzz.trimf(velocity_x.universe, [2, 4, 10])


    velocity_y['fast_up'] = fuzz.trimf(velocity_x.universe, [-10, -4, -2])
    velocity_y['slow_up'] = fuzz.trimf(velocity_x.universe, [-3, -1, 0])
    velocity_y['zero'] = fuzz.trimf(velocity_x.universe,      [-1, 0, 1])
    velocity_y['slow_down'] = fuzz.trimf(velocity_x.universe, [0, 1, 3])
    velocity_y['fast_down'] = fuzz.trimf(velocity_x.universe, [2, 4, 10])


    distance_x['far_left'] = fuzz.trimf(distance_x.universe, [-600, -400, -100])
    distance_x['close_left'] = fuzz.trimf(distance_x.universe, [-100, -50, 3])
    distance_x['zero'] = fuzz.trimf(distance_x.universe, [-5, 0, 5])
    distance_x['close_right'] = fuzz.trimf(distance_x.universe, [-3, 50, 100])
    distance_x['far_right'] = fuzz.trimf(distance_x.universe, [100, 400, 600])

    distance_y['far'] = fuzz.trimf(distance_y.universe, [100, 300, 600])
    distance_y['close'] = fuzz.trimf(distance_y.universe, [-50, 0, 200])

    angle['big_left'] = fuzz.trimf(angle.universe, [-90, -60, -50])
    angle['small_left'] = fuzz.trimf(angle.universe, [-60, -30, -5])
    angle['straight'] = fuzz.trimf(angle.universe, [-10, 0, 10])
    angle['small_right'] = fuzz.trimf(angle.universe, [5, 30, 60])
    angle['big_right'] = fuzz.trimf(angle.universe, [50, 60, 90,])

    rules = [

        ################################################################################
        # Rotation
        ################################################################################

        ctrl.Rule(distance_x['far_left'] & velocity_x['fast_left'], rotate['right']),
        ctrl.Rule(distance_x['far_left'] & velocity_x['fast_right'], rotate['left']),
        ctrl.Rule(distance_x['far_left'] & velocity_x['slow_right'], rotate['left']),
        ctrl.Rule(distance_x['far_left'] & velocity_x['slow_left'], rotate['left']),
        ctrl.Rule(distance_x['far_left'] & velocity_x['zero'], rotate['left']),

        ctrl.Rule(distance_x['far_right'] & velocity_x['fast_right'], rotate['left']),
        ctrl.Rule(distance_x['far_right'] & velocity_x['fast_left'], rotate['right']),
        ctrl.Rule(distance_x['far_right'] & velocity_x['slow_left'], rotate['right']),
        ctrl.Rule(distance_x['far_right'] & velocity_x['slow_right'], rotate['right']),
        ctrl.Rule(distance_x['far_right'] & velocity_x['zero'], rotate['right']),

        #####

        ctrl.Rule(distance_x['close_left'] & velocity_x['fast_left'], rotate['right']),
        ctrl.Rule(distance_x['close_left'] & velocity_x['fast_right'], rotate['left']),
        ctrl.Rule(distance_x['close_left'] & velocity_x['slow_left'], rotate['right']),
        ctrl.Rule(distance_x['close_left'] & velocity_x['slow_right'] , rotate['left']),

        ctrl.Rule(distance_x['close_left'] & velocity_x['slow_left'] & angle['small_left'] | angle['big_left'], rotate['right']),

        ctrl.Rule(distance_x['close_left'] & velocity_x['zero'] & angle['small_left'], rotate['right']),
        ctrl.Rule(distance_x['close_left'] & velocity_x['zero'] & angle['small_right'], rotate['left']),

        ctrl.Rule(distance_x['close_right'] & velocity_x['fast_right'], rotate['left']),
        ctrl.Rule(distance_x['close_right'] & velocity_x['fast_left'], rotate['right']),
        ctrl.Rule(distance_x['close_right'] & velocity_x['slow_right'], rotate['left']),
        ctrl.Rule(distance_x['close_right'] & velocity_x['slow_left'], rotate['right']),

        ctrl.Rule(distance_x['close_right'] & velocity_x['slow_right'] & angle['small_right'] | angle['big_right'], rotate['left']),

        ctrl.Rule(distance_x['close_right'] & velocity_x['zero'] & angle['small_right'] | angle['big_right'], rotate['left']),
        ctrl.Rule(distance_x['close_right'] & velocity_x['zero'] & angle['small_left'] | angle['big_left'], rotate['right']),

        #####

        ctrl.Rule(distance_x['zero'] & velocity_x['zero'] & angle['small_left'], rotate['right']),
        ctrl.Rule(distance_x['zero'] & velocity_x['zero'] & angle['small_right'], rotate['left']),

        ################################################################################
        # Thrust
        ################################################################################

        ctrl.Rule(angle['straight'] & velocity_y['zero'], thrust['off']),
        ctrl.Rule(angle['straight'] & velocity_y['slow_down'], thrust['off']),
        ctrl.Rule(angle['straight'] & velocity_y['fast_down'], thrust['on']),
        ctrl.Rule(angle['straight'] & velocity_y['slow_up'], thrust['off']),
        ctrl.Rule(angle['straight'] & velocity_y['fast_up'], thrust['off']),


        #####

        ctrl.Rule(angle['big_right'] & distance_y['close'], thrust['on']),
        ctrl.Rule(angle['big_left'] & distance_y['close'], thrust['on']),

        ctrl.Rule(angle['big_right'] & distance_y['far'], thrust['off']),
        ctrl.Rule(angle['big_left'] & distance_y['far'], thrust['off']),


        ctrl.Rule(angle['small_right'] & distance_y['close'], thrust['on']),
        ctrl.Rule(angle['small_left'] & distance_y['close'], thrust['on']),

        ctrl.Rule(angle['small_right'] & distance_y['far'], thrust['off']),
        ctrl.Rule(angle['small_left'] & distance_y['far'], thrust['off']),

    ]

    autopilot_ctrl = ctrl.ControlSystem(rules)
    return autopilot_ctrl


def fuzzy_control(rocket, platform, autopilot_ctrl):
    """
    Wykonuje sterowanie rozmyte rakietą przy użyciu systemu sterowania rozmytego autopilota.

    Metoda pobiera bieżące dane wejściowe, takie jak odległość w osi X i Y między rakietą a platformą, prędkości w osiach X i Y oraz kąt rakiety.
    Wartości te są wprowadzane do symulacji systemu rozmytego, a następnie obliczane są wyjścia sterujące: załączenie ciągu (thrust) i kierunek obrotu (rotate).
    Wyniki wyjściowe są zaokrąglane i stosowane w celu dostosowania stanu rakiety (np. włączenie ciągu lub obrót rakiety w odpowiednim kierunku).

    Parameters:
        rocket (Rocket): Obiekt rakiety, który ma być sterowany.
        platform (Platform): Obiekt platformy lądowania używany do określenia odległości.
        autopilot_ctrl (ControlSystem): System sterowania rozmytego skonfigurowany wcześniej do sterowania autopilotem rakiety.
    """

    distance_x_input, distance_y_input = Game.get_distance(rocket, platform)
    velocity_x_input = rocket.vel_x
    velocity_y_input = rocket.vel_y
    angle_input = rocket.angleDegrees

    # Create control system
    autopilot_simulation = ctrl.ControlSystemSimulation(autopilot_ctrl)

    # Input values
    autopilot_simulation.input['distance_x'] = distance_x_input
    autopilot_simulation.input['distance_y'] = distance_y_input
    autopilot_simulation.input['velocity_x'] = velocity_x_input
    autopilot_simulation.input['velocity_y'] = velocity_y_input
    autopilot_simulation.input['angle'] = angle_input

    # Compute the fuzzy output
    autopilot_simulation.compute()

    thrust_output = autopilot_simulation.output['thrust']
    rotate_output = autopilot_simulation.output['rotate']

    rounded_thrust_output = int(round(thrust_output, 0))
    rounded_rotate_output = int(round(rotate_output, 0))

    # Apply the computed thrust and rotation
    # print(rounded_thrust_output)
    if rounded_thrust_output > 0:
        rocket.thrusting = True
        rocket.apply_thrust()
    else:
        rocket.thrusting = False

    # print(rounded_rotate_output)
    if rounded_rotate_output < 0:
        rocket.rotate("left")
    elif rounded_rotate_output > 0:
        rocket.rotate("right")

import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
import pygame
from pygame import mixer

# Konfiguracja detekcji oczu
EYE_AR_THRESH = 0.25  # Próg zamkniętych oczu
EYE_AR_CONSEC_FRAMES = 15  # Liczba klatek, przez które oczy muszą być zamknięte

# Indeksy punktów charakterystycznych oczu w modelu dlib
LEFT_EYE_POINTS = list(range(36, 42))
RIGHT_EYE_POINTS = list(range(42, 48))


"""
Autorzy: Sebastian Kalwasiński, Karol Spica
Biblioteki:
-cv2
-dlib
-numpy
-scipy
-pygame

Opis:
Program służący do "zmuszania" użytkownika do oglądania przedstawionego materiału. 
Gdy wykryte zostanie zamknięcie oczu film zostaje zatrzymany a użytkownik otrzymuje 
komunikat dzwiękowy "OGLĄDAJ!"

Główne funkcje programu:
- Odtwarzanie/zatrzymywanie materiału wideo połączonego z dzwiękiem
- Śledzenie gałek ocznych użytkownika w celu wykrycia momentu w którym
  użytkownika przestaje oglądać prezentowany materiał
"""

def eye_aspect_ratio(eye):
    """
    Oblicza współczynnik otwarcia oczu (EAR - Eye Aspect Ratio).

    EAR to wskaźnik, który mierzy stosunek wysokości do szerokości oka.
    Jeśli wartość EAR spada poniżej pewnego progu, oznacza to, że oczy są zamknięte.

    :param eye: Lista współrzędnych punktów konturu oka
    :return: Wartość współczynnika EAR
    """
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)


def initialize_system():
    """
    Inicjalizuje kamerę, detektor twarzy i system dźwiękowy.

    :return: Krotka zawierająca obiekty: cap_camera, cap_video, detector, predictor, watch_sound, frame_width, frame_height
    """
    pygame.init()
    mixer.init()

    # Inicjalizacja kamery i wideo
    cap_camera = cv2.VideoCapture(0)
    cap_video = cv2.VideoCapture("data/never.avi")

    # Pobranie wymiarów obrazu
    frame_width = int(cap_camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap_camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Inicjalizacja detektora twarzy i predyktora punktów charakterystycznych
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("data/shape_predictor_68_face_landmarks.dat")

    # Ładowanie dźwięków
    mixer.music.load("data/never.mp3")
    mixer.music.play(-1, 0.0)  # Odtwarzanie w pętli
    watch_sound = mixer.Sound("data/watch.mp3")

    return cap_camera, cap_video, detector, predictor, watch_sound, frame_width, frame_height


def process_frame(frame, detector, predictor):
    """
    Przetwarza pojedynczą klatkę wideo, wykrywa twarz i zwraca współczynnik otwarcia oczu (EAR).

    :param frame: Obraz z kamery
    :param detector: Model detekcji twarzy dlib
    :param predictor: Model predykcji punktów charakterystycznych dlib
    :return: EAR (średnia wartość dla obu oczu) lub None, jeśli twarz nie została wykryta
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 0)

    if len(faces) == 0:
        return None  # Brak twarzy na obrazie

    face = faces[0]  # Zakładamy jedną twarz
    landmarks = predictor(gray, face)

    left_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in LEFT_EYE_POINTS]
    right_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in RIGHT_EYE_POINTS]

    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)

    return (left_ear + right_ear) / 2.0


def update_video_display(cap_video, frame_cam, paused):
    """
    Wyświetla obraz łączący nagranie z kamery i pliku wideo.

    Jeśli oczy użytkownika są zamknięte, wyświetla pustą klatkę zamiast wideo.

    :param cap_video: Obiekt wideo OpenCV
    :param frame_cam: Obraz z kamery
    :param paused: Flaga pauzy
    :return: Połączony obraz (kamera + wideo)
    """
    if not paused:
        ret_vid, frame_vid = cap_video.read()
        if not ret_vid:
            cap_video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart filmu
            ret_vid, frame_vid = cap_video.read()
    else:
        frame_vid = np.zeros_like(frame_cam)  # Pusta klatka podczas pauzy

    # Dopasowanie wymiarów i połączenie obrazów
    frame_vid_resized = cv2.resize(frame_vid, (frame_cam.shape[1], frame_cam.shape[0]))
    combined_frame = np.hstack((frame_cam, frame_vid_resized))

    cv2.imshow("Camera and Video", combined_frame)
    return combined_frame


def release_resources(cap_camera, cap_video):
    """
    Zwalnia zasoby systemowe, zamyka okna i wyłącza dźwięk.

    :param cap_camera: Obiekt kamery OpenCV
    :param cap_video: Obiekt wideo OpenCV
    """
    cap_camera.release()
    cap_video.release()
    pygame.quit()
    cv2.destroyAllWindows()


def main():
    """
    Główna pętla programu, która obsługuje wykrywanie oczu, sterowanie odtwarzaniem i wyświetlanie obrazu.
    """
    cap_camera, cap_video, detector, predictor, watch_sound, frame_width, frame_height = initialize_system()

    paused = False
    frame_counter = 0

    while True:
        ret_cam, frame_cam = cap_camera.read()
        if not ret_cam:
            break

        ear = process_frame(frame_cam, detector, predictor)

        if ear is not None:
            if ear < EYE_AR_THRESH:
                frame_counter += 1
                if frame_counter >= EYE_AR_CONSEC_FRAMES:
                    cv2.putText(frame_cam, "Eyes Closed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    mixer.music.pause()
                    watch_sound.play()
                    paused = True
            else:
                frame_counter = 0
                cv2.putText(frame_cam, "Eyes Open", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                mixer.music.unpause()
                paused = False

        update_video_display(cap_video, frame_cam, paused)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    release_resources(cap_camera, cap_video)


if __name__ == "__main__":
    main()

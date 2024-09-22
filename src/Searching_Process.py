import sys
import time
import os
import tempfile
import numpy as np
import cv2
from PIL import ImageGrab  # Für Screenshots
import pyautogui

# Template-Bilder global laden
turnstile_template_path = os.path.join(os.path.dirname(__file__), '../img/Turnstile_Captcha.jpg')
turnstile_template = cv2.imread(turnstile_template_path, cv2.IMREAD_GRAYSCALE)

captcha2_template_path = os.path.join(os.path.dirname(__file__), '../img/Captcha2.jpg')
captcha2_template = cv2.imread(captcha2_template_path, cv2.IMREAD_GRAYSCALE)


def solve_turnstile(screenshot):
    # Screenshot ist bereits ein NumPy-Array
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Template Matching
    result = cv2.matchTemplate(screenshot_gray, turnstile_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Setze den Schwellenwert für die Übereinstimmung
    locations = np.where(result >= threshold)

    if locations[0].size > 0:
        # Positionen finden und ausgeben
        for pt in zip(*locations[::-1]):  # Umkehren der Koordinaten

            # Berechne die Klick-Position
            click_x = pt[0] + 30  # 30px nach rechts
            click_y = pt[1] + turnstile_template.shape[0] // 2  # Mitte des Templates

            print(f"Found Turnstile and click on position: {click_x}, {click_y}")

            pyautogui.click(click_x, click_y)


def solve_captcha2(screenshot):
    # Screenshot ist bereits ein NumPy-Array
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Template Matching für das Captcha in Graustufen
    result = cv2.matchTemplate(screenshot_gray, captcha2_template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= 0.8)  # Schwellenwert für das Haupt-Captcha

    scale_factor = 0.8  # Skalierungsfaktor

    if locations[0].size > 0:

        for pt in zip(*locations[::-1]):  # Umkehren der Koordinaten
            # Berechne die Region für das Captcha
            h, w = captcha2_template.shape
            captcha_region = screenshot[pt[1]:pt[1] + h, pt[0]:pt[0] + w]

            # Definierte Koordinaten für die weiteren 5 Bilder
            coordinates = [
                (145, 10, 60, 60),  # (x, y, width, height) - erstes Bild
                (65, 110, 50, 50),
                (120, 110, 50, 50),
                (175, 110, 60, 50),
                (235, 110, 60, 50)
            ]

            # Das erste Bild ausschneiden
            first_region = captcha_region[coordinates[0][1]:coordinates[0][1] + coordinates[0][3],
                           coordinates[0][0]:coordinates[0][0] + coordinates[0][2]]

            # Das erste Bild um den Faktor 0.8 verkleinern
            new_size = (int(first_region.shape[1] * scale_factor), int(first_region.shape[0] * scale_factor))
            resized_first_region = cv2.resize(first_region, new_size)

            best_match_value = -1
            match_location = None

            # Die restlichen 4 Bilder ausschneiden und vergleichen
            for i, (x, y, width, height) in enumerate(coordinates[1:], 1):
                cut_region = captcha_region[y:y + height, x:x + width]

                # Vergleich des verkleinerten ersten Bildes mit dem aktuellen Bild
                match_result = cv2.matchTemplate(cut_region, resized_first_region, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)

                # Suche nach der besten Übereinstimmung
                if max_val > best_match_value:
                    best_match_value = max_val
                    match_location = (x, y)
                    best_region_index = i  # Speichere den Index des besten Symbols

            click_x = pt[0] + match_location[0] + coordinates[1][2] // 2
            click_y = pt[1] + match_location[1] + coordinates[1][3] // 2

            print(f"Found Captcha2 and click on Symbol: {best_region_index}")

            pyautogui.click(click_x, click_y)


def main():
    global temp_dir
    temp_dir = tempfile.gettempdir()

    # Verarbeite die übergebenen Argumente
    stop_flag_path = sys.argv[1]  # Abbruchflag-Dateipfad als erstes Argument
    active_captchas = sys.argv[2:]  # Alle übergebenen Captcha-Namen

    while True:
        # Überprüfe, ob das Abbruchflag existiert
        if os.path.exists(stop_flag_path):
            print("Captcha Solver stopped.")
            os.remove(stop_flag_path)
            break

        # Screenshot erstellen und als NumPy-Array verarbeiten
        screenshot = np.array(ImageGrab.grab())  # Screenshot des gesamten Bildschirms

        # Übergeben des Screenshots an die entsprechenden Captcha-Funktionen
        for captcha in active_captchas:
            if captcha == "Turnstile":
                solve_turnstile(screenshot)
            elif captcha == "Captcha2":
                solve_captcha2(screenshot)
            else:
                print(f"Undefined Captcha: {captcha}")

        time.sleep(5)  # Warte 5 Sekunden, bevor der nächste Screenshot erstellt wird


if __name__ == "__main__":
    main()

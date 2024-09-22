import sys
import time
import os
import tempfile  # Für temporäre Dateien
import numpy as np
import cv2
from PIL import ImageGrab  # Für Screenshots
import pyautogui

# Template-Bilder global laden
turnstile_template_path = os.path.join(os.path.dirname(__file__), '../img/Turnstile_Captcha.jpg')
turnstile_template = cv2.imread(turnstile_template_path, cv2.IMREAD_GRAYSCALE)

captcha2_template_path = os.path.join(os.path.dirname(__file__), '../img/Captcha2.jpg')
captcha2_template = cv2.imread(captcha2_template_path, cv2.IMREAD_GRAYSCALE)


def solve_turnstile(screenshot_path):
    # Screenshot laden und in Graustufen umwandeln
    screenshot = cv2.imread(screenshot_path)
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

            print(f"Found Turnstile captcha and making a click on position: ({click_x}, {click_y})")

            pyautogui.click(click_x, click_y)


def solve_captcha2(screenshot_path):
    # Screenshot laden und in Graustufen umwandeln
    screenshot = cv2.imread(screenshot_path)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Template Matching für das Captcha in Graustufen
    result = cv2.matchTemplate(screenshot_gray, captcha2_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Setze den Schwellenwert für die Übereinstimmung
    locations = np.where(result >= threshold)

    if locations[0].size > 0:
        print("Found Captcha2 the solution for that coming soon.")

        for pt in zip(*locations[::-1]):  # Umkehren der Koordinaten
            # Berechne die Region für das Captcha
            h, w = captcha2_template.shape
            captcha_region = screenshot[pt[1]:pt[1] + h, pt[0]:pt[0] + w]

            # Zeige das gefundene Captcha an (optional)
            # cv2.imshow("Found Captcha2", captcha_region)
            # cv2.waitKey(0)  # Warte auf eine Taste, bevor das Fenster geschlossen wird

            # Definierte Koordinaten für die weiteren 5 Bilder
            coordinates = [
                (145, 10, 60, 60),  # (x, y, width, height)
                (65, 110, 50, 50),
                (120, 110, 50, 50),
                (175, 110, 60, 50),
                (235, 110, 60, 50)
            ]

            # Das erste Bild ausschneiden
            first_region = captcha_region[coordinates[0][1]:coordinates[0][1] + coordinates[0][3],
                           coordinates[0][0]:coordinates[0][0] + coordinates[0][2]]

            # Zeige das erste Bild an
            # cv2.imshow("First Region", first_region)
            # cv2.waitKey(0)  # Warte auf eine Taste, bevor das Fenster geschlossen wird

            # Die restlichen 4 Bilder ausschneiden
            for i, (x, y, width, height) in enumerate(coordinates[1:], 1):
                cut_region = captcha_region[y:y + height, x:x + width]

                # Zeige die ausgeschnittene Region an
                # cv2.imshow(f"Cut Region {i + 1}", cut_region)
                # cv2.waitKey(0)

            # cv2.destroyAllWindows()  # Schließe alle Fenster


def main():
    global temp_dir
    temp_dir = tempfile.gettempdir()
    screenshot_count = 0

    # Verarbeite die übergebenen Argumente
    stop_flag_path = sys.argv[1]  # Abbruchflag-Dateipfad als erstes Argument
    active_captchas = sys.argv[2:]  # Alle übergebenen Captcha-Namen

    while True:
        # Überprüfe, ob das Abbruchflag existiert
        if os.path.exists(stop_flag_path):
            print("Captcha Solver stopped.")
            os.remove(stop_flag_path)
            break

        # Screenshot erstellen
        screenshot_count += 1
        screenshot_path = os.path.join(temp_dir, f"screenshot_{screenshot_count}.png")
        screenshot = ImageGrab.grab()  # Screenshot des gesamten Bildschirms
        screenshot.save(screenshot_path)  # Speichern des Screenshots
        print("Screenshot made.")

        # Übergeben des Screenshots an die entsprechenden Captcha-Funktionen
        for captcha in active_captchas:
            if captcha == "Turnstile":
                solve_turnstile(screenshot_path)
            elif captcha == "Captcha2":
                solve_captcha2(screenshot_path)
            else:
                print(f"Undefined Captcha: {captcha}")

        time.sleep(5)  # Warte 5 Sekunden, bevor der nächste Screenshot erstellt wird


if __name__ == "__main__":
    main()

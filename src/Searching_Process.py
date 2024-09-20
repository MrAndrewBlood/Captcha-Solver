import sys
import time
import os
import numpy as np
import cv2
from PIL import ImageGrab  # Für Screenshots
import tempfile  # Für temporäre Dateien
import pyautogui

def solve_turnstile(screenshot_path):

    # Lade das Template-Bild (stelle sicher, dass der Pfad korrekt ist)
    template_path = os.path.join(os.path.dirname(__file__), '../img/Turnstile_Captcha.jpg')
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Screenshot laden und in Graustufen umwandeln
    screenshot = cv2.imread(screenshot_path)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Template Matching
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Setze den Schwellenwert für die Übereinstimmung
    locations = np.where(result >= threshold)

    if locations[0].size > 0:
        # Positionen finden und ausgeben
        for pt in zip(*locations[::-1]):  # Umkehren der Koordinaten
            print(f"Turnstile Captcha gefunden bei Position: {pt}")
            # Berechne die Klick-Position
            click_x = pt[0] + 30  # 30px nach rechts
            click_y = pt[1] + template.shape[0] // 2  # Mitte des Templates

            print(f"Klicken bei Position: ({click_x}, {click_y})")
            # Optional: Zeichne ein Rechteck um das gefundene Template
            cv2.rectangle(screenshot, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)

            pyautogui.click(click_x, click_y)


def solve_recaptcha(screenshot_path):
    print("Löse reCAPTCHA...")
    time.sleep(2)  # Simuliert eine Bearbeitungszeit
    print(f"reCAPTCHA gelöst! Screenshot gespeichert unter: {screenshot_path}")

def solve_hcaptcha(screenshot_path):
    print("Löse hCaptcha...")
    time.sleep(2)  # Simuliert eine Bearbeitungszeit
    print(f"hCaptcha gelöst! Screenshot gespeichert unter: {screenshot_path}")

def main():
    # Erstelle ein temporäres Verzeichnis für Screenshots
    global temp_dir
    temp_dir = tempfile.gettempdir()
    screenshot_count = 0

    # Verarbeite die übergebenen Argumente
    active_captchas = sys.argv[1:]  # Alle übergebenen Captcha-Namen

    while True:
        # Screenshot erstellen
        screenshot_count += 1
        screenshot_path = os.path.join(temp_dir, f"screenshot_{screenshot_count}.png")
        screenshot = ImageGrab.grab()  # Screenshot des gesamten Bildschirms
        screenshot.save(screenshot_path)  # Speichern des Screenshots

        # Übergeben des Screenshots an die entsprechenden Captcha-Funktionen
        for captcha in active_captchas:
            if captcha == "Turnstile":
                solve_turnstile(screenshot_path)
            elif captcha == "reCAPTCHA":
                solve_recaptcha(screenshot_path)
            elif captcha == "hCaptcha":
                solve_hcaptcha(screenshot_path)
            else:
                print(f"Unbekanntes Captcha: {captcha}")

        time.sleep(5)  # Warte 5 Sekunden, bevor der nächste Screenshot erstellt wird

if __name__ == "__main__":
    main()

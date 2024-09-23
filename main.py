import tkinter as tk
from tkinter import Text
import os
import cv2
import time
import numpy as np
from PIL import ImageGrab
import pyautogui
import threading

# Stats global laden
session_turnstile_count = 0
session_captcha2_count = 0
session_icon_captcha_count = 0

# Gesamtanzahl initialisieren
total_turnstile_count = 0
total_captcha2_count = 0
total_icon_captcha_count = 0

running = False  # Variable, um die Ausführung zu steuern

stats_dir = os.path.join(os.path.dirname(__file__), 'data')
stats_file_path = os.path.join(stats_dir, 'stats.txt')

# Ensure the 'data' directory exists
os.makedirs(stats_dir, exist_ok=True)


def solve_turnstile(screenshot):
    # Screenshot ist bereits ein NumPy-Array
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, turnstile_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7  # Schwellenwert für die Übereinstimmung (zwischen 0.7 und 0.8)
    locations = np.where(result >= threshold)

    if locations[0].size > 0:
        # Nur die erste Übereinstimmung verwenden
        pt = (locations[1][0], locations[0][0])  # Erste Übereinstimmung
        click_x = pt[0] + 30  # 30px nach rechts
        click_y = pt[1] + turnstile_template.shape[0] // 2  # Mitte des Templates

        console_print(f"Found Turnstile and click on position: {click_x}, {click_y}")
        update_stats("Turnstile")
        pyautogui.click(click_x, click_y)


def solve_icon_captcha(screenshot):
    # Screenshot ist bereits ein NumPy-Array
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, iconCaptcha_template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= 0.6)

    if locations[0].size > 0:
        # Nur die erste Übereinstimmung verwenden
        pt = (locations[1][0], locations[0][0])
        h, w = iconCaptcha_template.shape
        captcha_region = screenshot[pt[1]:pt[1] + h, pt[0]:pt[0] + w]

        # Koordinaten für die 5 Teile
        coordinates = [
            (10, 40, 75, 90),
            (85, 40, 75, 90),
            (160, 40, 75, 90),
            (235, 40, 75, 90),
            (310, 40, 75, 90)
        ]

        min_score = float('inf')  # Initialisiere die minimale Matching Score
        best_match_index = None  # Um den Index des besten Bildes zu speichern

        # Vergleich jedes Teilbildes mit den anderen
        for i, (x, y, width, height) in enumerate(coordinates):
            cut_region = captcha_region[y:y + height, x:x + width]

            total_score = 0  # Zum Speichern der gesamten Matching Score

            # Vergleiche mit den anderen Bildern
            for j, (x2, y2, width2, height2) in enumerate(coordinates):
                if i != j:
                    other_region = captcha_region[y2:y2 + height2, x2:x2 + width2]
                    # Berechne die Übereinstimmung mit den anderen Teilen
                    score = cv2.matchTemplate(cut_region, other_region, cv2.TM_CCOEFF_NORMED).max()
                    total_score += score

            # Aktualisiere die minimale Matching Score
            if total_score < min_score:
                min_score = total_score
                best_match_index = i

        # Bestes Teil gefunden - hier könntest du auf die Koordinate klicken oder ausgeben
        best_x, best_y, best_w, best_h = coordinates[best_match_index]
        console_print(f"Found IconCaptcha and click on Symbol: {best_match_index}")
        update_stats("IconCaptcha")

        # Hier könntest du Mausaktionen integrieren, um auf das Teil zu klicken
        pyautogui.click(best_x + pt[0] + 30, best_y + pt[1] + 30)


def solve_captcha2(screenshot):
    # Screenshot ist bereits ein NumPy-Array
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, captcha2_template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= 0.7)  # Schwellenwert für das Haupt-Captcha
    scale_factor = 0.8  # Skalierungsfaktor

    if locations[0].size > 0:
        # Nur die erste Übereinstimmung verwenden
        pt = (locations[1][0], locations[0][0])  # Erste Übereinstimmung
        h, w = captcha2_template.shape
        captcha_region = screenshot[pt[1]:pt[1] + h, pt[0]:pt[0] + w]

        coordinates = [
            (145, 10, 60, 60),
            (65, 110, 50, 50),
            (120, 110, 50, 50),
            (175, 110, 60, 50),
            (235, 110, 60, 50)
        ]
        first_region = captcha_region[coordinates[0][1]:coordinates[0][1] + coordinates[0][3],
                       coordinates[0][0]:coordinates[0][0] + coordinates[0][2]]
        new_size = (int(first_region.shape[1] * scale_factor), int(first_region.shape[0] * scale_factor))
        resized_first_region = cv2.resize(first_region, new_size)

        best_match_value = -1
        match_location = None

        for i, (x, y, width, height) in enumerate(coordinates[1:], 1):
            cut_region = captcha_region[y:y + height, x:x + width]
            match_result = cv2.matchTemplate(cut_region, resized_first_region, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)

            if max_val > best_match_value:
                best_match_value = max_val
                match_location = (x, y)
                best_region_index = i

        click_x = pt[0] + match_location[0] + coordinates[1][2] // 2
        click_y = pt[1] + match_location[1] + coordinates[1][3] // 2
        console_print(f"Found Captcha2 and click on Symbol: {best_region_index}")
        update_stats("Captcha2")
        pyautogui.click(click_x, click_y)


def console_print(message):
    console.insert(tk.END, message + "\n")
    console.see(tk.END)


def toggle_button():
    global running
    if start_button['text'] == 'Start':
        # Überprüfen, ob mindestens ein Captcha ausgewählt ist
        if not turnstile_var.get() and not captcha2_var.get() and not icon_captcha_var.get():
            console_print("No Captcha selected. Please select a solver.")
            return

        start_button['text'] = 'Stop'
        running = True
        console_print("Captcha Solver started.")
        threading.Thread(target=search_captcha).start()  # Starte den Thread für die Schleife
    else:
        start_button['text'] = 'Start'
        console_print("Captcha Solver stopped.")
        running = False  # Stoppe die Schleife


def search_captcha():
    while running:
        screenshot = np.array(ImageGrab.grab())

        if turnstile_var.get():
            solve_turnstile(screenshot)
        if captcha2_var.get():
            solve_captcha2(screenshot)
        if icon_captcha_var.get():
            solve_icon_captcha(screenshot)

        time.sleep(3)


def load_total_stats():
    global total_turnstile_count, total_captcha2_count, total_icon_captcha_count
    try:
        with open(stats_file_path, "r") as f:
            data = f.readlines()
            total_turnstile_count = int(data[0].strip()) if len(data) > 0 else 0
            total_captcha2_count = int(data[1].strip()) if len(data) > 1 else 0
            total_icon_captcha_count = int(data[2].strip()) if len(data) > 2 else 0
    except FileNotFoundError:
        total_turnstile_count = 0
        total_captcha2_count = 0
        total_icon_captcha_count = 0


def save_total_stats():
    global total_turnstile_count, total_captcha2_count, total_icon_captcha_count
    with open(stats_file_path, "w") as f:
        f.write(f"{total_turnstile_count}\n")
        f.write(f"{total_captcha2_count}\n")
        f.write(f"{total_icon_captcha_count}\n")


def update_stats(captcha_type):
    global session_turnstile_count, session_captcha2_count, session_icon_captcha_count
    global total_turnstile_count, total_captcha2_count, total_icon_captcha_count

    if captcha_type == "Turnstile":
        session_turnstile_count += 1
        total_turnstile_count += 1
    elif captcha_type == "Captcha2":
        session_captcha2_count += 1
        total_captcha2_count += 1
    elif captcha_type == "IconCaptcha":
        session_icon_captcha_count += 1
        total_icon_captcha_count += 1

    session_stats_label.config(
        text=f"Captchas solved in this session:     Turnstile: {session_turnstile_count}     Captcha2: {session_captcha2_count}     IconCaptcha: {session_icon_captcha_count}")
    total_stats_label.config(
        text=f"Captchas solved in total:            Turnstile: {total_turnstile_count}     Captcha2: {total_captcha2_count}     IconCaptcha: {total_icon_captcha_count}")

    save_total_stats()


turnstile_template_path = os.path.join(os.path.dirname(__file__), 'assets/Turnstile.jpg')
turnstile_template = cv2.imread(turnstile_template_path, cv2.IMREAD_GRAYSCALE)

captcha2_template_path = os.path.join(os.path.dirname(__file__), 'assets/Captcha2.jpg')
captcha2_template = cv2.imread(captcha2_template_path, cv2.IMREAD_GRAYSCALE)

iconCaptcha_template_path = os.path.join(os.path.dirname(__file__), 'assets/IconCaptcha.jpg')
iconCaptcha_template = cv2.imread(iconCaptcha_template_path, cv2.IMREAD_GRAYSCALE)

load_total_stats()

window = tk.Tk()
window.title("Captcha Solver")

width = 870
height = 420
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

window.geometry(f"{width}x{height}+{x}+{y}")

label = tk.Label(window, text="Please select the captchas you want to automatically solve, then click Start.")
label.grid(row=0, column=0, pady=10, padx=10)

turnstile_var = tk.BooleanVar()
captcha2_var = tk.BooleanVar()
icon_captcha_var = tk.BooleanVar()

turnstile_checkbox = tk.Checkbutton(window, text="Cloudflare Turnstile", variable=turnstile_var)
turnstile_checkbox.grid(row=1, column=0, padx=30, sticky='w')

capture2_checkbox = tk.Checkbutton(window, text="Captcha2 (EarnNow and other sites)", variable=captcha2_var)
capture2_checkbox.grid(row=1, column=0, padx=20)

icon_captcha_checkbox = tk.Checkbutton(window, text="IconCaptcha", variable=icon_captcha_var)
icon_captcha_checkbox.grid(row=1, column=0, padx=50, sticky='e')

start_button = tk.Button(window, text="Start", command=toggle_button)
start_button.grid(row=2, column=0, pady=10)

console = Text(window, height=10, width=80)
console.grid(row=3, column=0, pady=10)
window.grid_columnconfigure(0, weight=1)

session_stats_label = tk.Label(window,
                               text=f"Captchas solved in this session:      Turnstile: {session_turnstile_count}     Captcha2: {session_captcha2_count}     IconCaptcha: {session_icon_captcha_count}")
session_stats_label.grid(row=4, column=0, sticky='w', padx=25)

total_stats_label = tk.Label(window,
                             text=f"Captchas solved in total:                 Turnstile: {total_turnstile_count}     Captcha2: {total_captcha2_count}     IconCaptcha: {total_icon_captcha_count}")
total_stats_label.grid(row=5, column=0, sticky='w', padx=25)

window.mainloop()

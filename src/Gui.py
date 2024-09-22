import tkinter as tk
import sys
import io
import subprocess
import threading
import queue
import os
import tempfile


class GUI:
    def __init__(self):
        # Zähle gelöste Captchas in der aktuellen Sitzung
        self.session_turnstile_count = 0
        self.session_captcha2_count = 0

        # Gesamtanzahl aus Datei laden oder initialisieren
        self.total_turnstile_count = 0
        self.total_captcha2_count = 0
        self.load_total_stats()

        # Erstelle das Hauptfenster
        self.window = tk.Tk()
        self.window.title("Captcha Solver")

        # Berechne die Position für die Mitte des Bildschirms
        width = 700
        height = 330
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Setze die Größe und Position des Fensters
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        # Erstelle eine Beschreibung oberhalb der Checkboxen
        self.description_label = tk.Label(self.window,
                                          text="Please choose the Captchas that you want to solve automatically and then click Start.")
        self.description_label.grid(row=0, column=0, padx=10, pady=10)

        # Erstelle einen Frame für die Checkboxen und Labels
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=1, column=0, padx=170, sticky="w")
        self.turnstile_var = tk.BooleanVar()
        self.checkbox_turnstile = tk.Checkbutton(self.frame, text="Cloudflare Turnstile", variable=self.turnstile_var)
        self.checkbox_turnstile.grid(row=0, column=0, sticky="w")

        # Erstelle einen Frame für die Checkboxen und Labels
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=1, column=0, padx=80, sticky="e")
        self.captcha2_var = tk.BooleanVar()
        self.checkbox_captcha2 = tk.Checkbutton(self.frame, text="Captcha2 (EarnNow and other sites)", variable=self.captcha2_var)
        self.checkbox_captcha2.grid(row=0, column=0, sticky="w")

        # Erstelle einen Start-Button
        self.start_button = tk.Button(self.window, text="Start", command=self.toggle_button)
        self.start_button.grid(row=3, column=0, pady=10)

        # Erstelle ein Text-Widget für die Konsole
        self.console = tk.Text(self.window, height=10, width=80)
        self.console.grid(row=4, column=0, pady=10)
        self.window.grid_columnconfigure(0, weight=1)

        # Beschriftungen für gelöste Captchas pro Sitzung
        self.session_stats_label = tk.Label(self.window,
                                            text=f"Captchas solved this session:   Turnstile: {self.session_turnstile_count}   Captcha2: {self.session_captcha2_count}")
        self.session_stats_label.grid(row=5, column=0, padx=25, sticky="w")

        # Beschriftungen für gelöste Captchas insgesamt
        self.total_stats_label = tk.Label(self.window,
                                          text=f"Captchas solved all time:   Turnstile: {self.total_turnstile_count}   Captcha2: {self.total_captcha2_count}")
        self.total_stats_label.grid(row=5, column=0, padx=25, sticky="e")

        # Umleiten von print-Ausgaben zur Konsole
        sys.stdout = StreamToTextWidget(self.console)

        # Statusvariable, ob das Programm läuft oder nicht
        self.is_running = False
        self.output_queue = queue.Queue()  # Für die Ausgabe vom Prozess

        # Startet den Thread für das Auslesen der Konsole
        self.window.after(100, self.process_queue)

    def load_total_stats(self):
        # Lade die Gesamtstatistik aus einer Datei
        try:
            with open("stats.txt", "r") as f:
                data = f.readlines()
                self.total_turnstile_count = int(data[0].strip())
                self.total_captcha2_count = int(data[1].strip())
        except FileNotFoundError:
            # Wenn die Datei nicht existiert, starte mit 0
            self.total_turnstile_count = 0
            self.total_captcha2_count = 0

    def save_total_stats(self):
        # Speichere die Gesamtstatistik in eine Datei
        with open("stats.txt", "w") as f:
            f.write(f"{self.total_turnstile_count}\n")
            f.write(f"{self.total_captcha2_count}\n")

    def update_stats(self, captcha_type):
        if captcha_type == "Turnstile":
            self.session_turnstile_count += 1
            self.total_turnstile_count += 1
        elif captcha_type == "Captcha2":
            self.session_captcha2_count += 1
            self.total_captcha2_count += 1

        # Aktualisiere die GUI-Anzeige
        self.session_stats_label.config(
            text=f"Captchas solved this session:   Turnstile: {self.session_turnstile_count}   Captcha2: {self.session_captcha2_count}")
        self.total_stats_label.config(
            text=f"Captchas solved all time:   Turnstile {self.total_turnstile_count}   Captcha2 {self.total_captcha2_count}")

        # Speichere die Gesamtstatistik
        self.save_total_stats()

    def toggle_button(self):
        if not self.is_running:
            self.start_action()
        else:
            self.stop_action()

    def start_action(self):
        if not (self.turnstile_var.get() or self.captcha2_var.get()):
            print("No Captcha selected. Please select a solver.")
            self.start_button.config(text="Start")
            self.is_running = False
        else:
            args = []
            if self.turnstile_var.get():
                args.append("Turnstile")
            if self.captcha2_var.get():
                args.append("Captcha2")

            print(f"Start searching and solving: {args}")
            threading.Thread(target=self.run_process, args=(args,), daemon=True).start()
            self.start_button.config(text="Stop")
            self.is_running = True

    def run_process(self, args):
        # Startet den Prozess
        self.stop_flag_path = os.path.join(tempfile.gettempdir(), "stop_flag.txt")  # Pfad für das Abbruchsignal
        process = subprocess.Popen(['python', 'Searching_Process.py', self.stop_flag_path] + args,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            self.output_queue.put(line)  # Fügt die Ausgabe zur Queue hinzu
        process.stdout.close()
        process.wait()

        # Prozess ist beendet
        self.is_running = False
        self.start_button.config(text="Start")

    def process_queue(self):
        try:
            while True:
                line = self.output_queue.get_nowait()
                print(line.strip())

                # Aktualisiere die Statistiken basierend auf der Ausgabe
                if "Found Turnstile" in line:
                    self.update_stats("Turnstile")
                elif "Found Captcha2" in line:
                    self.update_stats("Captcha2")

        except queue.Empty:
            pass
        finally:
            self.window.after(100, self.process_queue)

    def stop_action(self):
        print("Please wait until Captcha Solver stopping...")
        # Abbruchflag erstellen
        with open(self.stop_flag_path, 'w') as f:
            f.write('stop')  # Signal zum Stoppen
        self.is_running = False
        self.start_button.config(text="Start")

    def run(self):
        self.window.mainloop()


class StreamToTextWidget(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass


# Hauptprogramm starten
if __name__ == "__main__":
    gui = GUI()
    gui.run()

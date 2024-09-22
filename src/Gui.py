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
        # Erstelle das Hauptfenster
        self.window = tk.Tk()
        self.window.title("Captcha Solver")

        # Berechne die Position für die Mitte des Bildschirms
        width = 700
        height = 400
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Setze die Größe und Position des Fensters
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        # Erstelle eine Beschreibung oberhalb der Checkboxen
        self.description_label = tk.Label(self.window,
                                          text="Please choose the Captchas that you want to solve automatically and then click Start.")
        self.description_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Erstelle einen Frame für die Checkboxen und Labels
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Erstelle Checkboxen mit Labels
        self.turnstile_var = tk.BooleanVar()
        self.captcha2_var = tk.BooleanVar()

        # Checkboxen erstellen
        self.checkbox_turnstile = tk.Checkbutton(self.frame, text="Cloudflare Turnstile", variable=self.turnstile_var)
        self.checkbox_turnstile.grid(row=0, column=0, sticky="w")
        self.checkbox_captcha2 = tk.Checkbutton(self.frame, text="Captcha2 (EarnNow and other sites)", variable=self.captcha2_var)
        self.checkbox_captcha2.grid(row=1, column=0, sticky="w")

        # Erstelle einen Start-Button
        self.start_button = tk.Button(self.window, text="Start", command=self.toggle_button)
        self.start_button.grid(row=3, column=0, pady=10)

        # Erstelle ein Text-Widget für die Konsole
        self.console = tk.Text(self.window, height=10, width=80)
        self.console.grid(row=4, column=0, pady=10)
        self.window.grid_columnconfigure(0, weight=1)

        # Umleiten von print-Ausgaben zur Konsole
        sys.stdout = StreamToTextWidget(self.console)

        # Statusvariable, ob das Programm läuft oder nicht
        self.is_running = False
        self.output_queue = queue.Queue()  # Für die Ausgabe vom Prozess

        # Startet den Thread für das Auslesen der Konsole
        self.window.after(100, self.process_queue)

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
        except queue.Empty:
            pass
        finally:
            self.window.after(100, self.process_queue)  # Überprüfe die Queue wieder in 100 ms

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

# Captcha Solver

A Python-based automated Captcha Solver developed using OpenCV and PyAutoGUI. This tool can recognize and automatically
solve various types of Captchas.

## Features

- Real-time statistics on solved Captchas for the current Session and Overall
- User-friendly GUI for selecting Captchas and controlling the solving process
- Supports this Captcha types:

| Captcha                            | Success Rate |
|------------------------------------|:------------:|
| Cloudflare Turnstile               |     99%      |
| Captcha2 (EarnNow and other sites) |     90%      |
| IconCaptcha                        |     20%      |

## Usage

1. Select the captchas you want to solve automatically.
2. Click "Start" to begin the solving process.
3. Click "Stop" to end the solving process.
4. Check the statistics in the GUI to see how many captchas have been solved.

**IMPORTANT**

It cannot work headless, you must see the captcha everytime in the screen that it works.

## Installation

Download and start the compiled .exe or

1. Install the Requirements

2. Download or Clone the repository:

```
git clone https://github.com/MrAndrewBlood/Captcha-Solver.git
```

3. Navigate to the project directory:

```
cd Captcha-Solver
```

4. Ensure that the captcha templates are present in the `assets` directory. The templates should include the following
   files:
    - Turnstile.jpg
    - Captcha2.jpg
    - IconCaptcha1.jpg


5. Run the script:

```
python main.py
```

## Requirements

- "Git" for cloning
- Python 3.x
- Required packages:
    - OpenCV (opencv-python)
    - NumPy (numpy)
    - Pillow (Pillow)
    - PyAutoGUI (pyautogui)
    - Tkinter (typically included with Python)
    - Requests (requests)

You can install the required packages using pip:

```
pip install numpy opencv-python Pillow pyautogui requests
```

## Planned

+ Add a menu bar
+ Release for Linux/Mac

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.
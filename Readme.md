## Usage

+ Install the Requirements
+ Download or clone the repository
```
git clone https://github.com/MrAndrewBlood/Captcha-Solver.git
```
+ Start the main.py
```
cd Captcha-Solver
python main.py
```
## Requirements

+ Git for cloning
+ Python with pip

```
pip install numpy opencv-python Pillow pyautogui
```

## How it works

After starting, it takes every second a screenshot and search with opencv template matching for the activated captchas if it finds one, it clicks on that. 

**IMPORTANT**

It cannot work headless, you must see the captcha everytime in the screen that it works.

## Included Captchas

| Captcha              | Success Rate |
|----------------------|:------------:|
| Cloudflare Turnstile |     99%      |
| Captcha2             |     90%      |
| IconCaptcha          |     20%      |

## Planned

+ Release for Linux/Mac
## Usage

+ Install the Requirements
+ Download or clone the repository
```
git clone https://github.com/MrAndrewBlood/Captcha-Solver.git
```
+ Start the Main.py in the src folder
```
cd Captcha-Solver/src
python Main.py
```
## Requirements

+ Git for cloning
+ Python with pip
```
pip install numpy
pip install opencv-python
pip install pillow
pip install pyautogui
```

## How it works

After starting, it takes every 5 seconds a screenshot and search with opencv template matching for the activated captchas if it finds one, it clicks on that. 

**IMPORTANT**

It cannot work headless, you must see the captcha everytime in the screen that it works.

## How it works

Included Captchas:

| Captcha              | Success Rate  |
|----------------------|---------------|
| Cloudflare Turnstile | 99%           |
| Captcha2             | 90%           |

## Planned

+ Better structure and Readme
+ Add statistic infos
+ Version control on startup
+ Release for win/linux/mac
+ Add more Captchas
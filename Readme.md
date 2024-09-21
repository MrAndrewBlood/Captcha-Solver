## Usage

+ Install the Requirements
+ Download or clone the repository
+ Start the Main.py in the src folder


## Requirements

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

## Planned

+ Better structure and Readme
+ Add statistic infos
+ Version control on startup
+ Release for win/linux/mac
+ Add mor Captchas
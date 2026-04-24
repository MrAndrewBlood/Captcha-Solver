# Captcha Solver

A Python-based automated Captcha Solver developed using OpenCV and PyAutoGUI. This tool can recognize and automatically
solve various types of Captchas.

## Features

- Compiled .exe available, so no need to install dependencies
- Version check on startup
- Real-time statistics on solved Captchas for the current Session and Overall
- User-friendly GUI for selecting Captchas and controlling the solving process
- Supports this Captcha types:

| Captcha                            | Success Rate |
|------------------------------------|:------------:|
| Cloudflare Turnstile               |     99%      |
| Captcha2 (EarnNow and other sites) |     90%      |
| IconCaptcha                        |     20%      |

<!-- 
=============================================================
⚠️ PROPOSAL FOR ADVERTISING / SPONSORSHIP ⚠️

Hi! I'd like to place this advertisement in your repository.
If you're interested in sponsorship or advertising, please contact me:

📱 Telegram: @keropo
🔗 LinkedIn: https://www.linkedin.com/in/kirill-ponomarev-k/

This is just a proposal — feel free to reject or modify!
=============================================================
-->

<!-- AD -->
---
## Sponsors

✅ CapMonster.Cloud — Fast, Reliable CAPTCHA Solving for Automation & Scraping

[![CapMonster Cloud](https://help.zennolab.com/upload/u/02/020538b7c128.png)](https://capmonster.cloud/en/?utm_source=github&utm_campaign=MrAndrewBlood_Captcha-Solver)

If you are tired of wasting time solving endless CAPTCHAs during scraping, automation, or testing — we’ve got a solution for you.  
Meet CapMonster.Cloud — the AI-powered CAPTCHA solving service trusted by thousands of users worldwide. 🚀

--

🔥 **Why users love CapMonster.Cloud**
  
💡 Very high success rates (up to 99%)  
⚡ Super fast solving times  
💲 Affordable transparent pricing (pay per 1,000 CAPTCHAs)  
🔌 Easy integration via API + browser extensions  
⭐ Excellent reviews on TrustPilot, SourceForge, SaaSHub, AlternativeTo

--

🔗 **Useful Links**

💲 [Pricing & Supported CAPTCHA Types (25+ types supported)](https://capmonster.cloud/en?utm_source=github&utm_campaign=MrAndrewBlood_Captcha-Solver#new-plans)  
📘 [API Documentation](https://docs.capmonster.cloud/?utm_source=github&utm_campaign=MrAndrewBlood_Captcha-Solver)  
💡 Main Website → [capmonster.cloud](https://capmonster.cloud/en/?utm_source=github&utm_campaign=MrAndrewBlood_Captcha-Solver)  
⭐ Reviews → [TrustPilot](https://www.trustpilot.com/review/capmonster.cloud)

---
<!-- /AD -->

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

or compile your own .exe

```
pip install pyinstaller
build_pyinstaller.bat
```

## Requirements

- "Git" for cloning the repository
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

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

# 🎮 Call of Duty Matchmaking Automation Bot

A Python-based automation bot that handles **matchmaking, relogging, and quitting** in Call of Duty (tested with Party Games & Gunfight modes).  
Built with **PyAutoGUI + keyboard hooks**, it detects on-screen UI elements and simulates clicks to automate repetitive tasks.

---

## ✨ Features
- 🖱️ Image-based UI automation:
  - Matchmaking navigation (`Find Match` → `Party Games` → `Gunfight`)
  - Relogging if gamertag not detected
  - Auto-quit or wait for the other team
- 🎮 Hotkeys:
  - **F8** → Start automation  
  - **F7** → Pause/Stop automation  
  - **ESC** → Exit program
- 🔄 Smart behavior:
  - Gamertag check before starting  
  - Kick/quit handling with retries  
  - Configurable quit/wait toggle (`quitSwitch`)  
- 🖼️ Supports **image confidence levels** (tolerates minor UI differences)

---

## 🛠️ Tech Stack
- [pyautogui](https://pyautogui.readthedocs.io/en/latest/) – screen recognition & clicking  
- [keyboard](https://github.com/boppreh/keyboard) – global hotkeys  
- [threading](https://docs.python.org/3/library/threading.html) – background key listener  

---

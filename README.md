# ScreenPrivacyLock

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5.x-green?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Tasks-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Defense](https://img.shields.io/badge/Defense-Real--Time%20AI-red?style=for-the-badge)
![AutoLock](https://img.shields.io/badge/Auto--Lock-20s%20Timeout-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**Your personal AI bodyguard for desktop privacy and confidentiality.**  
*Protects against prying eyes in offices, cafes, libraries, and public workspaces by automatically cloaking your screen with opaque frosted blur and locking after 20 seconds of user absence.*

[Key Features](#-key-features) • [What's New in v2.1](#-whats-new-in-v21) • [Quick Start](#-quick-start) • [Controls & Gestures](#-tactical-controls--hotkeys) • [Configuration](#-configuration--tuning) • [Credits](#-author--credits)

</div>

---

## ⚡ Overview

**Smart Sentinel** is an autonomous AI workstation defense daemon that monitors your physical surroundings using a standard webcam. It continuously identifies the **primary authorized operator** and detects when an unauthorized person looks over your shoulder (**shoulder-surfing / lurking**). 

The instant a second person is detected, Sentinel immediately engages a **100% Opaque Frosted Screen Blur** across your entire display, sounds a cyber alert, and captures photographic evidence of the intruder. When the lurker walks away, your desktop is automatically restored. If you are working with a friend or colleague, simply show a **Thumbs-Up gesture** to authorize them! Furthermore, if you step away from your desk, Sentinel automatically locks Windows (`Win + L`) after 20 seconds.

---

## 🚀 What's New in v2.1 (Enhanced Accuracy & Motion Freedom)

1. ⏱️ **20-Second Walk-Away Auto-Lock**: When you step away from your camera, Sentinel provides a generous 20-second countdown (with an audio warning at 15s) before locking Windows (`Win + L`). If you return anytime before 20s, the timer instantly cancels!
2. 📐 **100% Full-Frame Camera Capture Area**: Active scanning boundaries widened to 100% of the camera's field of view (`0.0` to `1.0`). You can freely move left, right, up, down, or lean without being clipped out.
3. 🧠 **Inertial Tracking Memory (No Flicker on Movement)**: Built-in 18-frame (~0.6s) tracking memory. Momentary head tilts, nose scratches, blinks, or speaking will never cause false "USER_ABSENT" alarms.
4. 🔄 **Dual-Cascade Fusion (Frontal + Profile)**: Automatically engages profile face detection (both left and right via horizontal flipping) if you turn your head sideways.
5. 💡 **CLAHE Adaptive Lighting Equalization**: Automatically balances uneven shadows, bright windows, and dark room lighting in real-time.
6. 🌫️ **100% Opaque Real Frosted Glass Blur**: Replaced semi-transparent cloaks with full-screen snapshot Gaussian frosted blur (`-alpha 1.0`). All background windows, code, and confidential text are completely obscured.
7. 👍 **Thumbs-Up Companion Authorization Gesture**: If someone behind you is a friend or colleague, simply show a **Thumbs-Up** to the camera to authorize them and dismiss the blur.

---

## 🌟 Key Features

- 👁️ **Multi-Person Shoulder-Surfing Defense**: Distinguishes the primary user from peripheral lurkers using fast multi-scale facial tracking.
- 🌫️ **Instant Frosted Privacy Blur**: Spawns a full-screen, 100% opaque dark frosted shield that completely obscures confidential code, chats, or financial records.
- 👍 **Gesture Trust Companion Mode**: Primary operator can authorize trusted peers on the fly using a simple webcam Thumbs-Up gesture.
- 🚪 **Walk-Away Auto-Locker**: Automatically locks Windows (`Win + L`) after 20 seconds of user absence, preventing unattended workstation access.
- 📸 **Automatic Intruder Evidence Capture**: Silently snaps a photo of anyone peeking over your shoulder and saves it with a timestamp into the `intruders/` directory.
- 🔊 **Synthesized Cyber Audio Alerts**: Plays non-blocking tactical alerts when a threat is detected and ascending confirmation chimes when authorized or re-secured.
- 🎯 **Cinematic Tactical HUD & Radar**: Live camera feed displaying targeting brackets, operator verification, real-time threat DEFCON levels, and rotating radar blips.
- 🕵️ **Stealth Mode**: Press `[S]` to run Sentinel 100% invisibly in the background with zero camera window on screen.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch Smart Sentinel
```bash
python main.py
```

### 3. Startup Calibration
Look directly at the webcam for 3 seconds while the calibration HUD scans and locks your facial profile (0% -> 100%). Once calibrated, the Sentinel is fully armed!

---

## ⌨️ Tactical Controls & Hotkeys

| Key / Gesture | Action | Description |
|:---:|:---|:---|
| 👍 **Thumbs-Up Gesture** | **Authorize Companion** | Show Thumbs-Up when blurred to authorize friend/colleague and unblur screen |
| **`[ Q ]`** / **`[ Esc ]`** | **Master Quit** | Safely shuts down Sentinel and cleans up camera resources |
| **`[ C ]`** | **Test Privacy Blur** | Manually toggles the full-screen frosted privacy shield for demonstration |
| **`[ T ]`** | **Trust Companion (Key)** | Keyboard shortcut to authorize companion if gesture is not preferred |
| **`[ R ]`** | **Reset Trust** | Revokes companion authorization and returns Sentinel to maximum security |
| **`[ L ]`** | **Instant Lock** | Instantly locks the Windows computer (`Win + L`) |
| **`[ S ]`** | **Stealth Mode** | Toggles camera preview on/off for silent background operation |

---

## 🔧 Configuration & Tuning

All settings are centralized in `sentinel/config.py`:

```python
# Startup Calibration Duration (seconds)
CALIBRATION_SECONDS     = 3.0

# Absence Auto-Lock (20 seconds)
AUTO_LOCK_ENABLED       = True
ABSENCE_TIMEOUT_SECONDS = 20.0  # Lock workstation 20s after user leaves camera
ABSENCE_WARNING_SECONDS = 15.0  # Warning audio beep at 15s

# 100% Full-Frame Capture Area
ACTIVE_ZONE_TOP         = 0.00
ACTIVE_ZONE_BOTTOM      = 1.00
ACTIVE_ZONE_LEFT        = 0.00
ACTIVE_ZONE_RIGHT       = 1.00

# Head Motion Freedom & Sensitivity
CASCADE_MIN_NEIGHBORS   = 4     # High sensitivity, accommodates natural speech & movement
FACE_PERSISTENCE_FRAMES = 18    # ~0.6s inertial tracking memory
```

---

<div align="center">

## 👨‍💻 Author & Credits

### **MADE BY — Soumya Shrichandani**


⭐ **Star this repository if you care about real-world AI privacy & automation!** ⭐

</div>

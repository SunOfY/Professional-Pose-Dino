# 🦖 Professional Pose Dino

Professional Pose Dino is an AI-powered remake of the classic Chrome Dinosaur Game using:

* 🎮 Pygame
* 📷 OpenCV
* 🤖 MediaPipe Pose
* 🧠 Real-time body gesture control

Instead of using keyboard controls, the player controls the dinosaur using body movement detected through a webcam.

This project combines:

* Computer Vision
* Pose Detection
* Real-time Webcam Processing
* AI Interaction
* Game Development

---

# ✨ Features

* ✅ Original Chrome Dino physics preserved
* ✅ Real-time webcam overlay
* ✅ MediaPipe Pose tracking
* ✅ Shoulder-based jump detection
* ✅ Duck detection
* ✅ Clap-to-start calibration system
* ✅ Bird + cactus obstacles
* ✅ Smooth pose tracking
* ✅ Score system
* ✅ Game over / restart system
* ✅ Exportable `.exe`

---

# 🎮 How To Play

The game uses your body movement instead of keyboard input.

## Calibration

Before starting:

1. Stand in front of the webcam
2. Clap your hands 👏
3. The system will calibrate your neutral body position

After calibration:

| Action  | Movement                  |
| ------- | ------------------------- |
| Jump    | Raise shoulders / body up |
| Duck    | Lower shoulders / crouch  |
| Restart | Clap again                |

---

# 🧠 How Pose Detection Works

The project uses:

* Google MediaPipe Pose
* OpenCV webcam capture
* Real-time shoulder tracking

The game calculates:

* Shoulder center position
* Jump threshold
* Duck threshold
* Body movement smoothing

Pose landmarks are processed frame-by-frame from the webcam feed.

---

# 🛠 Technologies Used

| Technology  | Purpose                   |
| ----------- | ------------------------- |
| Python      | Main programming language |
| Pygame      | Game engine               |
| OpenCV      | Webcam processing         |
| MediaPipe   | Human pose estimation     |
| PyInstaller | EXE export                |

---

# ⚠ Important Compatibility Notes

## Recommended Python Version

This project is tested and stable on:

```text
Python 3.10
```

Recommended:

```text
Python 3.10.x (64-bit)
```

---

## MediaPipe Compatibility

MediaPipe has compatibility limitations.

Recommended version:

```text
mediapipe==0.10.14
```

---

## Known Issues

MediaPipe may NOT work correctly with:

* Python 3.12
* Some Python 3.11 environments
* Some ARM devices
* Older Windows Visual C++ runtimes

If you encounter installation errors, use:

```text
Python 3.10
```

---

# 📦 Installation

## 1. Clone Repository

```bash
git clone https://github.com/SunOfY/Professional-Pose-Dino.git
cd Professional-Pose-Dino
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install pygame
pip install opencv-python
pip install mediapipe==0.10.14
pip install pyinstaller
```

Or:

```bash
pip install -r requirements.txt
```

---

# ▶ Run Game

```bash
python main.py
```

---

# 🖥 Export To EXE

## Debug Build

```bash
pyinstaller --collect-all mediapipe --collect-all cv2 --add-data "Assets;Assets" main.py
```

---

## Release Build

```bash
pyinstaller --onefile --windowed --collect-all mediapipe --collect-all cv2 --add-data "Assets;Assets" main.py
```

Generated file:

```text
dist/main.exe
```

---

# 📁 Project Structure

```text
Professional-Pose-Dino/
│
├── Assets/
│   ├── Bird/
│   ├── Cactus/
│   ├── Dino/
│   └── Other/
│
├── build/
├── dist/
├── main.py
├── main.spec
├── build_exe.bat
├── preview.png
└── README.md
```

---

# 🙏 Credits & Inspiration

## Original Chrome Dinosaur Game

Special thanks to the creators of the original Chrome Dinosaur Game for the timeless gameplay concept and obstacle mechanics.

---

## Chrome Dino Tutorial Inspiration

Part of the game structure and gameplay implementation was inspired by Chrome Dino tutorials from the programming community.

---

## MediaPipe / Pose Detection Inspiration

The MediaPipe pose control system in this project was heavily inspired by:

* MiAI VN tutorials
* MediaPipe learning videos
* Computer Vision examples using OpenCV + MediaPipe

I learned many important concepts about:

* Pose landmark tracking
* Webcam coordinate systems
* Real-time body detection
* OpenCV frame processing
* Gesture-based interaction

from MiAI VN educational content and examples.

This project is a personal experimental project created for learning and entertainment purposes.

---

# 📸 Preview

<img width="1913" height="869" alt="preview" src="https://github.com/user-attachments/assets/6c176bad-ee9c-44c6-acde-dcd62cda78b8" />

---

# 🚀 Future Improvements

* Full hand tracking
* Better gesture recognition
* Multiplayer mode
* AI difficulty scaling
* Mobile camera support
* Gesture customization
* Full-screen support

---

# ⭐ Support

If you like this project:

* Give it a ⭐ on GitHub
* Fork the repository
* Improve the gameplay
* Create your own gesture controls

Thank you for checking out Professional Pose Dino 🦖

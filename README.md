# Virtual Painter - Hand Gesture Controlled Drawing App
> This project is an interactive virtual painter powered by OpenCV and MediaPipe. You can draw, select colors, and erase on screen using only your hand gestures--no mouse or keyboard required!

---

# Features

- Drawing Mode -> Use index finger only to draw on the canvas
- Selection Mode -> Use index + middle fingers to select tools/colors from the toolbar.
- Erase Mode -> Show all fingers up to erase content
- Toolbar -> Choose between multiple colors (red, green, blue, yellow).
- Save Option -> Save your artwork with a single key press
- Keyboard Shortcuts:
    - q -> Quit
    - c -> Clear Canvas
    - s -> Save canvas as image

---

# Tech Stack
- Python 3.x
- OpenCV 
- MediaPipe

---

# Project Structure
```
VirtualPainter/
│
├── src/
│   ├── app.py               # Main application
│   ├── config.py            # Config values (camera index, thresholds, etc.)
│   ├── drawing/
│   │   ├── canvas.py        # Canvas and drawing logic
│   │   └── tools.py         # Helper functions (finger detection, FPS, etc.)
│   └── hand_tracking/
│       └── tracker.py       # Hand landmark tracking using MediaPipe
│
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

---

# Installation
1. Clone the repository:
    ```
    git clone https://github.com/your-username/virtual-painter.git
    cd virtual-painter
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the application:
    ```
    python src/app.py
    ```

---

# Future Improvements
- Add Undo/Redo with swipe gestures
- Improve erser tool (soft brush instead of straight lines).
- Add more colors and brush sizes.
- Support for multi-hand drawing.

---

# License
This project is open-source and available under the MIT License

---




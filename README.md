Virtual Keyboard Using Python, OpenCV, and MediaPipe
This project implements a virtual keyboard that allows users to type on a screen using hand gestures, without the need for a physical keyboard.

📌 Core Features
Hand tracking using MediaPipe Hands to detect fingers and gestures in real-time.

OpenCV used for capturing webcam input and rendering the keyboard UI.

Finger tip detection to simulate "key press" when the index finger reaches a virtual key region.

Visual feedback to highlight the key being "pressed."

Configurable keyboard layout rendered directly on the video feed.

Supports text entry simulation that can be displayed or saved.

🛠️ Technologies Used
Python – Main programming language

OpenCV – For video processing and UI rendering

MediaPipe – For efficient hand and finger tracking

🎯 How It Works
The webcam captures the user's hand.

MediaPipe processes the frame to detect and track hand landmarks.

The fingertip of the index finger is used to detect a "hover" or "click" on keys.

A bounding box is drawn for each key, and key presses are registered based on the fingertip position and gesture.

✅ Use Cases
Contactless typing in public/shared environments

Assistive tech for people with limited mobility

Experimentation with computer vision and gesture recognition

📦 Optional Enhancements
Add sound feedback or haptic vibration (via external hardware).

Use machine learning for more advanced gesture recognition.

Multilingual keyboard layouts.


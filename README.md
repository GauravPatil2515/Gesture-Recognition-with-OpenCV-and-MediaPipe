# Gesture Recognition with OpenCV and MediaPipe

This project demonstrates how to use hand gesture recognition to interact with a computer. The system detects hand gestures like the "Peace" sign and, if recognized as valid, triggers a countdown to take a selfie using the webcam. The selfie is saved without annotations (like countdown text) to a folder named `selfies`.

## Features
- Detects hand gestures using **MediaPipe**.
- Recognizes gestures such as:
  - **Peace Sign (index and middle fingers extended)**: Triggers the selfie function.
- **3-second Countdown** before taking a selfie.
- **Selfie Saving**: The captured selfie is stored in the `selfies/` directory.
- The program exits when the **'q' key** is pressed.

## How It Works
1. The program uses **OpenCV** to access the webcam.
2. It employs **MediaPipe Hands** to detect and track hand landmarks.
3. Hand gestures are classified based on the relative position of the hand landmarks:
   - If a valid gesture (Peace Sign) is detected, a 3-second countdown begins.
   - After 3 seconds, the program captures a selfie without any annotations (text or overlays).
4. The captured selfie is saved in a folder named `selfies`, with the filename formatted as `selfie_YYYYMMDD_HHMM.jpg`.

## Prerequisites
- Python 3.x
- OpenCV
- MediaPipe

### Installation
1. Clone the repository or download the project.
   ```bash
   git clone <repository-url>

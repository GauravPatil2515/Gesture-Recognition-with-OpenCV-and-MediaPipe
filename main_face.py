import cv2
import mediapipe as mp
import os
from datetime import datetime
import time

# Initialize MediaPipe Hands and Drawing Utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Capture video from the webcam
cap = cv2.VideoCapture(0)  # 0 for the default webcam

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open video capture")
    exit()

# Function to save selfie
def save_selfie(frame):
    # Create directory to store selfies if it doesn't exist
    selfie_dir = 'selfies'
    if not os.path.exists(selfie_dir):
        os.makedirs(selfie_dir)

    # Create a unique file name based on timestamp
    filename = os.path.join(selfie_dir, f'selfie_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg')

    # Save the image (without annotations)
    cv2.imwrite(filename, frame)
    print(f"Selfie saved as {filename}")

# Initialize variables for the timer
countdown_started = False
countdown_start_time = 0

# Initialize the hand detection model with confidence thresholds
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break

        # Flip the frame horizontally for a selfie-view display
        frame = cv2.flip(frame, 1)

        # Create a clean copy of the frame before adding any annotations
        clean_frame = frame.copy()

        # Convert the frame from BGR (OpenCV format) to RGB (MediaPipe format)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame to detect hands
        results = hands.process(rgb_frame)

        # Set the default message to "Invalid"
        gesture_text = 'Invalid'

        # If hand landmarks are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get finger landmark positions
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_base = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

                # Detect "Peace" gesture (index and middle finger extended)
                if (index_tip.y < index_mcp.y and middle_tip.y < middle_mcp.y and
                        ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y):
                    gesture_text = 'Valid'

                    # Start the countdown if it's not already started
                    if not countdown_started:
                        countdown_started = True
                        countdown_start_time = time.time()

        # Display the gesture status (Valid/Invalid) on the frame
        cv2.putText(frame, gesture_text, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if gesture_text == 'Valid' else (0, 0, 255), 2, cv2.LINE_AA)

        # Handle the countdown timer
        if countdown_started:
            # Calculate the elapsed time
            elapsed_time = time.time() - countdown_start_time
            remaining_time = max(3 - int(elapsed_time), 0)

            # Display the countdown on the screen
            cv2.putText(frame, f"Taking selfie in {remaining_time}s", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # If 3 seconds have passed, take the selfie
            if elapsed_time >= 3:
                save_selfie(clean_frame)  # Save the clean frame without annotations
                countdown_started = False  # Reset the countdown after taking the selfie

        # Show the frame with the gesture classification and countdown
        cv2.imshow('Gesture Recognition', frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
from time import sleep
from pynput.keyboard import Controller
import numpy as np
import cvzone

#Initialize Video Capture and set frame size
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

#Initialize Mediapipe Hand Detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

#Keyboard layout
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["CLR", "<-", "SPACE"]]

finalText = ""

# Initialize virtual keyboard
keyboard = Controller()

# Function to draw the keyboard layout
def drawAll(img, buttonList):
    overlay = img.copy()  # Create a copy of the original image for the overlay
    alpha = 0.5  #Transparency factor

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # Draw the key rectangle on the overlay
        cvzone.cornerRect(overlay, (x, y, w, h), 20, rt=0)
        cv2.rectangle(overlay, button.pos, (x + w, y + h), (67, 65, 65), cv2.FILLED)
        cv2.putText(overlay, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    # Blend the overlay with the original image
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    return img

# Class for button properties
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Create a list of buttons for each key in the keyboard layout
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        # Make "CLR", "<-", and "SPACE" buttons wider and position them on the last row
        if key == "CLR":
            buttonList.append(Button([50, 100 * i + 50], key, size=[200, 85]))  # Adjusted width for "CLR"
        elif key == "<-":
            buttonList.append(Button([300, 100 * i + 50], key, size=[200, 85]))  # Adjusted width for "<-"
        elif key == "SPACE":
            buttonList.append(Button([550, 100 * i + 50], key, size=[500, 85]))  # Wider spacebar button
        else:
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))  # Regular keys

# Function to detect hand landmarks and return index finger tip position
def get_hand_landmarks(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    lm_list = []
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return lm_list

# Main loop
while True:
    success, img = cap.read()  # Read frame from webcam
    if not success:
        break  # Exit if frame is not captured

    lm_list = get_hand_landmarks(img)  # Get landmark positions of the hand

    img = drawAll(img, buttonList)  # Draw the keyboard layout

    if lm_list:  # If hand is detected
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # Check if the index finger tip (id=8) is within the button area
            if len(lm_list) > 8 and x < lm_list[8][1] < x + w and y < lm_list[8][2] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                # Measure distance between index finger tip (id=8) and middle finger tip (id=12)
                x1, y1 = lm_list[8][1], lm_list[8][2]  # Index finger tip
                x2, y2 = lm_list[12][1], lm_list[12][2]  # Middle finger tip
                length = np.hypot(x2 - x1, y2 - y1)

                # If fingers are close enough, simulate a key press
                if length < 30:
                    if button.text == "CLR":
                        finalText = ""  # CLR the input text
                    elif button.text == "<-":
                        finalText = finalText[:-1]  # Remove the last character
                    elif button.text == "SPACE":
                        finalText += " "  # Add a space character
                    else:
                        keyboard.press(button.text)
                        finalText += button.text
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    sleep(0.3)  # Add a small delay

    # Display the typed text on screen below the keyboard
    cv2.rectangle(img, (50, 500), (1200, 600), (67, 65, 65), cv2.FILLED)  # New position below the keyboard
    cv2.putText(img, finalText, (60, 580), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Show the frame
    cv2.imshow("Virtual Keyboard", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()

import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""
keyboard = Controller()

class Button():
    def __init__(self, pos, text, size = [80,80]):
        self.pos = pos
        self.size = size
        self.text = text

    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        # Draw the rectangle and put the text
        cv2.rectangle(img, self.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, self.text, (x + 20, y + 65),
            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        return img

def drawALL(img, buttonList):
    for button in buttonList:
        img = button.draw(img)
    return img

buttonList = []
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        buttonList.append(Button([100 * x + 50, 100 + i * 100], key))
button_clicked = False
while True:
    success, img = cap.read()
    if success:
        hands, img = detector.findHands(img)  # Get the modified image
        result = detector.findPosition(img)
        lmList = []  # Define lmList here

        img = drawALL(img, buttonList)

        if result is not None:
            lmList, bboxInfo = result
            print(lmList)
        else:
            print("No position found in the image.")

        if lmList:  # Now you can use lmList here
            for button in buttonList:
                x, y = button.pos
                w,h = button.size

                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw = False)
                    print(l)

                    if l<30 and not button_clicked:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                        keyboard.press(button.text)
                        keyboard.release(button.text)
                        button_clicked = True
                    elif l>30:
                        button_clicked = False
        cv2.rectangle(img, (50, 450), (700, 550), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finalText, (60, 525),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)


        cv2.imshow('Image', img) # Display the frame

        # Exit on pressing 'x'
        if cv2.waitKey(1) == ord('x'):
            break
    else:
        print("Failed to capture a frame.")
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
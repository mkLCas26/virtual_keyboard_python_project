# Project Title: AI Virtual Keyboard using Python
# Date Started: Feb 27, 2025
# Date Finished: Feb 28, 2025


# Importing Libraries
import cv2 
from cvzone.HandTrackingModule import HandDetector
from time import sleep

# For Launching Camera
cap = cv2.VideoCapture(0)
cap.set(3,1950)
cap.set(4,720)

# Hand Detection + Keyboard Letters + Text String Initialization
detector = HandDetector(detectionCon=0.8 , maxHands=2)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["SPACE", "BACK"]]
finalText = ""

# Draw Buttons on the Keyboard
def drawALL(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img 

# Button Class for Defining Keys
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Creating Keys and Layout + Attributes
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        #buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
        if key == "SPACE":
            buttonList.append(Button([300, 100 * i + 50], key, size=(265, 75)))
        elif key == "BACK":
            buttonList.append(Button([600 * j + 50, 100 * i + 50], key, size=(210,75)))
        else: 
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Loop for Keyboard Function
while True:                                                    # For reading the camera frame
    success, img = cap.read()

    if not success:                                            # For camera failure
        print("Failed to grab Camera")
        break

    img = cv2.flip(img,1)                                      # Flip Camera for Mirrored Frame

    # Hands detection within the frame
    hands, img = detector.findHands(img, flipType=False)       # debug trial to match cvzone and mediapipe version + updated function usage
    if hands:
        lmList = hands[0]["lmList"]
        bbox = hands[0]['bbox']
    else:
        lmList = []

    img = drawALL(img, buttonList)

    # Check if finger is within a button 
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # Checks if Index Fingertip (Landmark 8) is within a button
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                 cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                 cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                 l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])
                 print(l)

                # Indicates that we close 2 fingers = keypress
                 if l<30:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    # Keypress append and remove function (text output)
                    if button.text == "SPACE":
                        finalText = finalText + " "
                    elif button.text == "BACK":
                        finalText = finalText[:-1]
                    else: 
                        finalText += button.text

                    sleep(0.90)                               # For keypress delay 

    # Drawing textbox         
    cv2.rectangle(img, (70, 470), (1000, 680), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (70, 550), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    
    cv2.imshow("Image", img)

    # For easy dialog box exit : via pressing "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()                                   # For releasing camera
cv2.destroyAllWindows()                         # Closing OpenCV
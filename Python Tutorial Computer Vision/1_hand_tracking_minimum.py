import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(1)
mpHands = mp.solutions.hands.Hands()
mpDraw = mp.solutions.drawing_utils

while 1:
    success, img = cap.read()
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rst = mpHands.process(rgb)
    if (hands := rst.multi_hand_landmarks) is not None:
        for hand in hands:
            mpDraw.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)


    cv2.imshow("Img", img)
    cv2.waitKey(1)
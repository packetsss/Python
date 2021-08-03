"""
Get 4 corners of the img in Windows Paint
[235, 147] t-l
[370, 146] t-r
[202, 329] b-l
[350, 327] b-r
"""

import os
import cv2
import numpy as np

circle = np.zeros((4, 2), np.float32)
ct = 0


def mousePoints(event, x, y, flags, params):
    global ct
    if event == cv2.EVENT_LBUTTONDOWN:
        if ct == 4:
            return False
        circle[ct] = [x, y]
        ct += 1
        print(circle)


img = cv2.imread(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src/poker.jpg"))
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
while 1:

    if ct == 4:
        width, height = 250, 350
        # desired card size after warped to bird eye view

        pt1 = np.float32([[234, 147], [371, 146], [200, 331], [351, 330]])
        pt2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(circle, pt2)
        out = cv2.warpPerspective(img, matrix, (width, height))
        cv2.imshow("Warped img", out)
        break

    for i in range(4):
        cv2.circle(img, (int(circle[i][0]), int(circle[i][1])), 5, (0, 255, 0), cv2.FILLED)
        # draw all points out in the img

    cv2.imshow("Original img", img)
    cv2.setMouseCallback("Original img", mousePoints)  # connect mouse click to function
    cv2.waitKey(1)

cv2.waitKey()

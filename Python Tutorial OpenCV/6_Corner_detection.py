# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import cv2
import numpy as np

img = cv2.imread("src/chessboard.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 100, 0.2, 20)
# Shi-Tomasi Corner Detector
# img, # of best corners, minimum quality: 0(bad) --> 1(good), minimum euclidean distance: pythagorean theorem

corners = np.int0(corners)
# convert to int

for corner in corners:
    x, y = corner.ravel()
    # flatten the arr; [[3, 2]] or [[[3]], [[2]]] --> [3, 2]

    cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
    # draw circles in every corner

for i in range(len(corners)):
    for j in range(i + 1, len(corners)):
        corner1 = tuple(corners[i][0])
        # get 1st corner
        corner2 = tuple(corners[j][0])
        # get 2nd corner

        color = tuple(map(int, np.random.randint(0, 255, size=3)))
        # easier way to create a random color, output --> (129, 172, 85)

        cv2.line(img, corner1, corner2, color, 1)
        # connect every corner by lines


cv2.imshow("Image", img)
cv2.waitKey()
cv2.destroyAllWindows()

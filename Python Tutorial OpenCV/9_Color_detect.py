# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import cv2
import numpy as np

# img = cv2.imread("src/book.jpg")
# img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)

def empty(*args):
    pass


cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 340)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

while 1:
    img = cv2.imread("src/book.jpg")
    img = cv2.resize(img, (0, 0), fx=0.2, fy=0.2)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(img_hsv, lower, upper)

    rst = cv2.bitwise_and(img, img, mask=mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    hstack = np.hstack([img, mask, rst])

    # cv2.imshow("Original img", img)
    # cv2.imshow("HSV img", img_hsv)
    # cv2.imshow("MASK", mask)
    # cv2.imshow("RESULT", rst)
    cv2.imshow("HSTACK", hstack)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()

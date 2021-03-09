import cv2
import numpy as np


capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while 1:
    _, frame = capture.read()

    width = int(capture.get(3))
    height = int(capture.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # only picking up blue, extract color
    # mask it self is only b/w, 0/1

    result = cv2.bitwise_and(frame, frame, mask=mask)
    # bitwise operation:
    # 1, 1 -- > 1
    # 1, 0 -- > 0
    # 0, 1 -- > 0
    # 0, 0 -- > 0

    cv2.imshow("frame", result)
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

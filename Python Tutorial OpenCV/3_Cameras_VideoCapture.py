# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import numpy as np
import cv2

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while 1:
    _, frame = capture.read()

    width = int(capture.get(3))
    height = int(capture.get(4))
    # 3 --> width, 4 --> height

    image = np.zeros(frame.shape, np.uint8)
    # pre-allocate a window of black

    smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    # create a 1/4 sized frame

    image[:height // 2, :width // 2] = cv2.rotate(smaller_frame, cv2.cv2.ROTATE_180)
    image[height // 2:, :width // 2] = smaller_frame
    image[height // 2:, width // 2:] = cv2.rotate(smaller_frame, cv2.cv2.ROTATE_180)
    image[:height // 2, width // 2:] = smaller_frame
    # fit 4 smaller_frame to empty image, and flip 2 of them

    cv2.imshow("frame", image)
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
# free up the webcam

cv2.destroyAllWindows()

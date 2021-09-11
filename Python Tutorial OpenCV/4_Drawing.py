# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import cv2


capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while 1:
    _, frame = capture.read()

    width = int(capture.get(3))
    height = int(capture.get(4))

    img = cv2.line(frame, (0, 0), (width, height), (255, 0, 0), 10)
    # draw a line diagonal of the screen: img, (bot, top), (width, height), thickness)
    img = cv2.line(img, (width, 0), (0, height), (0, 0, 255), 10)
    img = cv2.rectangle(img, (100, 100), (200, 200), (0, 255, 0), 10)
    img = cv2.circle(img, (300, 300), 60, (128, 128, 128), -1)
    # -1 is solid

    font = cv2.FONT_HERSHEY_COMPLEX
    img = cv2.putText(img, "I like you", (200, height-100), font, 2, (0, 0, 0), 3, cv2.LINE_AA)
    # image, text, position, font, font scale(size), text thickness, line type

    cv2.imshow("frame", img)
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()

cv2.destroyAllWindows()

import cv2
import numpy as np


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # use CHAIN_APPROX none or simple

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= 2000:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 5)
            param = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * param, True)
            # print(len(approx))
            # indicates how many edges the shape has

            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
            # draw bounding box

            cv2.putText(imgContour, "Corners: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)


def empty(*args):
    pass


cv2.namedWindow("param")
cv2.resizeWindow("param", 640, 200)
cv2.createTrackbar("T1", "param", 214, 500, empty)
cv2.createTrackbar("T2", "param", 512, 512, empty)

while 1:
    img = cv2.imread("src/stop_sign.jpg")
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    imgContour = img.copy()

    t1 = cv2.getTrackbarPos("T1", "param")
    t2 = cv2.getTrackbarPos("T2", "param")
    imgCanny = cv2.Canny(imgGray, t1, t2)
    kernal = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernal, iterations=1)

    getContours(imgDil, imgContour)

    imgStack = stackImages(0.8, ([img, imgBlur, imgCanny], [imgDil, imgContour, imgContour]))
    cv2.imshow("Original img", imgStack)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()

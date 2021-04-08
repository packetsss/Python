import cv2
import numpy as np

frame = cv2.imread('Image_screenshot_05.04.2021.png')

height, width, _ = frame.shape

rgb = frame[int(height / 3):height, 0:width]

rgbsidefilter = {
    "lowR": 216,
    "highR": 255,
    "lowG": 222,
    "highG": 255,
    "lowB": 198,
    "highB": 255
}

lowR = rgbsidefilter["lowR"]
highR = rgbsidefilter["highR"]
lowG = rgbsidefilter["lowG"]
highG = rgbsidefilter["highG"]
lowB = rgbsidefilter["lowB"]
highB = rgbsidefilter["highB"]

lower = np.array([lowR, lowG, lowB])
higher = np.array([highR, highG, highB])
mask = cv2.inRange(rgb, lower, higher)

mid_y = mask.shape[0] // 2
canny = cv2.Canny(mask, 100, 100)
spot = np.where(canny[mid_y, :] == 255)[0]
mid_x = (np.max(spot) + np.min(spot)) // 2
cv2.circle(mask, (mid_x, mid_y), 5, (255, 0, 0), -1)

cv2.imshow("1", mask)
cv2.waitKey()

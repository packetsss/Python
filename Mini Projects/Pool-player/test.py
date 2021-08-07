import cv2
import numpy as np

img = cv2.imread("data/label/1628278194.7557938.jpg")

h, w = img.shape[:2]
ww = 0.496875 * w
hh = 0.527815 * h
www = 0.396875 * w / 2
hhh = 0.369064 * h / 2
print(h, w)
img = img[int(hh-hhh):int(hh+hhh), int(ww-www):int(ww+www)]

cv2.imshow("", img)
cv2.waitKey()
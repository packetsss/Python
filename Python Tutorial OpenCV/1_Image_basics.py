# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import cv2

img = cv2.imread('src/landscape.jpg', 0)
# -1 --> color, ignore transparency
# 0 --> gray_scale
# 1 --> unchanged

img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
# shrink size by half using fx, fy

img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
# rotate image

'''cv2.imwrite("new_img.jpg", img)'''
# store a image

cv2.imshow("Image", img)
# window name, image

cv2.waitKey(10000)
# time in ms --> 1000 = 1s
cv2.destroyAllWindows()

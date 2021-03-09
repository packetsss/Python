import cv2
import random

img = cv2.imread("src/landscape.jpg", 1)


'''print(type(img))'''
# numpy array

'''print(img.shape)'''
# height, width, channel(3, BGR) --> [blue, green, red] from 0 to 255

'''print(img[1][400])'''
# access a single pixal

'''for i in range(100):
    for j in range(img.shape[1]):
        img[i][j] = [random.randrange(255), random.randrange(255), random.randrange(255)]'''
# it becomes noise

tag = img[500:700, 600:900]
img[100:300, 500:800] = tag
# will copy a square of the array and paste it to another part of the image

cv2.imshow("1", img)
cv2.waitKey()


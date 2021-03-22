from PIL import Image
import cv2
import numpy as np
from timeit import default_timer as timer

im = cv2.imread("landscape.jpg")

s = timer()

im = Image.fromarray(np.uint8(im)).convert('RGB')

imr = im.rotate(22, expand=True, resample=Image.BICUBIC)

imr = np.array(imr)
e = timer()
print(e - s)
cv2.imshow("", imr)

cv2.waitKey()


import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
from Sudoku_extractor import Extract

img = Extract().extract_sudoku("src/board.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.imshow("1", img)
cv2.waitKey()

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
cfg = r"--oem 3 --psm 6 outputbase digits"
boxes = pytesseract.image_to_data(img, config=cfg)
img_h, img_w, _ = img.shape

for height in range(img_h // 9, img_h + 1, img_h // 9):
    new_img = img[height - img_h // 9:height, :]
    boxes = pytesseract.image_to_data(new_img, config=cfg)
    for i, box in enumerate(boxes.splitlines()):
        if i != 0:
            box = box.split()
            print(box)
            if len(box) == 12:
                x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
                cv2.rectangle(new_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(new_img, box[11], (x, y + 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 60, 220), 2)

    cv2.imshow("1", new_img)
    cv2.waitKey()

for i, box in enumerate(boxes.splitlines()):
    if i != 0:
        box = box.split()
        if len(box) == 12:
            # mask out all characters

            x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, box[11], (x, y + 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 60, 220), 2)


plt.imshow(img)
plt.show()

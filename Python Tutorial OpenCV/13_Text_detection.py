import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
img = cv2.imread("src/text.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# --- Detecting Characters --- #
'''
boxes = pytesseract.image_to_boxes(img)
img_h, img_w, _ = img.shape

for box in boxes.splitlines():

    box = box.split(' ')
    x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
    cv2.rectangle(img, (x, img_h - y), (w, img_h - h), (0, 0, 255), 2)
    cv2.putText(img, box[0], (x, img_h - y + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 60, 220), 2)
    
print(pytesseract.image_to_string(img))
'''

# --- Detecting Words --- #

cfg = r"--oem 1"
boxes = pytesseract.image_to_data(img, config=cfg)
img_h, img_w, _ = img.shape

for i, box in enumerate(boxes.splitlines()):
    if i != 0:
        box = box.split()
        if len(box) == 12:
            # mask out all characters

            x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, box[11], (x, y + 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 60, 220), 2)


# --- Detecting Numbers --- #
'''
cfg = r"--oem 3 --psm 6 outputbase digits"  # 
boxes = pytesseract.image_to_data(img, config=cfg)
img_h, img_w, _ = img.shape

for i, box in enumerate(boxes.splitlines()):
    if i != 0:
        box = box.split()
        if len(box) == 12:
            # mask out all characters

            x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, box[11], (x, y + 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 60, 220), 2)
'''

cv2.imshow("img", img)
cv2.waitKey()

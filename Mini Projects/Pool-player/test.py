import os
import cv2
import time
import numpy as np
from util import *
from yolov5.load_model import YoloModel

src = "data\\play"
dst = "data\\play_labeled"
files_list = os.listdir(src)

model = YoloModel().model

model.iou = 0.7
model.conf = 0.6
model.max_det = 18

boundary_coord = (34, -37, 43, -39)

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while 1:
# for file in files_list[::2]:
    center_list = []

    # img_path = os.path.join(src, file)
    # if img_path[-3:] != "jpg":
    #     continue

    # img = cv2.imread(img_path)
    r, img = capture.read()
    if r is None:
        continue

    # transform image
    height, width = img.shape[:2]
    img = img[130:height-40, 60:width-230]

    # wrap to table
    width, height = 900, 450

    pt1 = np.float32([[32, 11], [1594, 32], [9, 897], [1607, 867]])
    pt2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2) # use circle in 1st arg
    img = cv2.warpPerspective(img, matrix, (width, height))

    cropped_img = img[boundary_coord[0]:boundary_coord[1], boundary_coord[2]:boundary_coord[3]]

    result = model(cropped_img, size=960)
    result_img = result.render()[0]

    rects = result.xyxy[0].cpu().numpy()

    if rects is not None:
        prev_center = None
        i = 0
        while 1:
            rects[i, 0] += boundary_coord[2]
            rects[i, 2] += boundary_coord[2]
            rects[i, 1] += boundary_coord[0]
            rects[i, 3] += boundary_coord[0]

            x = rects[i, :]
            center = np.array([int((x[0] + x[2]) / 2), int((x[1] + x[3]) / 2)])
            if prev_center is not None and np.abs(center - prev_center).sum() < 10:
                if rects[i, 4] > rects[i - 1, 4]:
                    rects = np.delete(rects, i - 1, axis=0)
                else:
                    rects = np.delete(rects, i, axis=0)
                
            prev_center = center

            if i >= rects.shape[0] - 1:
                break
            i += 1
    
    # img_path = os.path.join(dst, file)
    # cv2.imwrite(img_path, img)

    if True:
    # with open(img_path[:-4] + ".txt", "a") as f:
        for x in rects:
            h, w = img.shape[:2]
            x_center, y_center = ((x[0] + x[2]) / 2) / w, ((x[1] + x[3]) / 2) / h
            confidence, classes = x[4], x[5]
            size = 21
            width, height = size / w, (size - 1) / h

            classes = 3
            str = f"{int(classes)} {x_center} {y_center} {width} {height}\n"
            # f.write(str)

            cv2.circle(img, (int((x[0] + x[2]) / 2), int((x[1] + x[3]) / 2)), 10, (255, 255, 255), 5)

    cv2.imshow("i", img)
    if cv2.waitKey(40) == ord('q'):
        break


cv2.destroyAllWindows()

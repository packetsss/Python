from util import *
from yolov5.load_model import YoloModel

import os
import cv2
import time
import numpy as np

src = "data\\yolo\\play"
files_list = os.listdir(src)


model = YoloModel().model

model.iou = 0.2
model.conf = 0.1
model.max_det = 20


boundary_coord = (34, -37, 43, -39)
table_sides = (boundary_coord[0], 900 + boundary_coord[1], boundary_coord[2], 450 + boundary_coord[3])


for file in files_list[::5]:
    img_path = os.path.join(src, file)
    if img_path[-3:] != "jpg":
        continue

    img = cv2.imread(img_path)

    cropped_img = img[boundary_coord[0]:boundary_coord[1], boundary_coord[2]:boundary_coord[3]]

    
    result = model(np.copy(img), size=700)
    rects = result.xyxy[0].cpu().numpy()
    centers = np.apply_along_axis(get_center_from_pred, 1, rects)
    
    cue_ball_info = rects[rects[:, 5] == 3]
    cue_ball_center = None if len(cue_ball_info) == 0 else get_center_from_pred(cue_ball_info[0])

    cue_info = rects[rects[:, 5] == 4]
    cue_center = None if len(cue_info) == 0 else get_center_from_pred(cue_info[0])
    '''
    cue_mask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), CUE_MASK[0], CUE_MASK[1])[:, :-23]
    cue_canny = cv2.GaussianBlur(cv2.Canny(cue_mask, 60, 60), (5, 5), cv2.BORDER_DEFAULT)
    lines = cv2.HoughLinesP(cue_canny, 1, np.pi/180, threshold=90, minLineLength=25, maxLineGap=5)

    start, end = None, None
    if lines is not None:
        m = max(lines, key=lambda l: distance_between_two_points(np.array([l[0][0], l[0][1]]), np.array([l[0][2], l[0][3]])))
        
        if point_in_rectangle(np.array([m[0][0], m[0][1]]), table_sides) or \
            point_in_rectangle(np.array([m[0][2], m[0][3]]), table_sides):
            ss, ee = np.array([m[0][0], m[0][1]]), np.array([m[0][2], m[0][3]])
        else:
            m = None
        
        pt1, pt2 = np.array([]), np.array([])
        for line in lines:
            x1, y1, x2, y2 = line[0]
            s, e = np.array([x1, y1]), np.array([x2, y2])

            slope = (y2 - y1) / (x2 - x1 + 1e-6)
            if -0.1 < slope < 0.1 and not point_in_rectangle(s, table_sides) and not point_in_rectangle(e, table_sides):
                continue
            if m is not None:
                if distance_between_two_points(ss, s) < 30 and distance_between_two_points(ee, e) < 30:
                    pt1 = np.append(pt1, ss)
                    pt1 = np.append(pt1, s)
                    pt2 = np.append(pt2, ee)
                    pt2 = np.append(pt2, e)
                    # cv2.line(img, line[0][:2], line[0][2:], MAGENTA, 1)
        
        if m is not None:
            pt1, pt2 = np.reshape(pt1, (-1, 2)), np.reshape(pt2, (-1, 2))
            start, end = np.rint(pt1.mean(axis=0)), np.rint(pt2.mean(axis=0))
            cv2.line(img, start.astype(int), end.astype(int), MAGENTA, 5)
        '''

    if cue_ball_center is not None and cue_center is not None:# start is not None and end is not None:
        # cue_ball_center[0] += boundary_coord[2]
        # cue_ball_center[1] += boundary_coord[0]

        # find_distance_to_cue_ball = lambda pt: np.linalg.norm(pt - cue_ball_center)
        # tip = min([start, end], key=find_distance_to_cue_ball).astype(int)
        tip = cue_center

        # calculate aiming line
        theta = np.arctan2(tip[1] - cue_ball_center[1], tip[0] - cue_ball_center[0])
        end_pt = (int(tip[0] - 900 * np.cos(theta)), int(tip[1] - 900 * np.sin(theta)))

        if point_in_rectangle(tip, table_sides):
            cv2.circle(img, tip, 7, CYAN, 5)
            cv2.line(img, cue_ball_center, end_pt, WHITE, 4)

    
    for x in rects:
        h, w = img.shape[:2]
        center = (int((x[0] + x[2]) / 2), int((x[1] + x[3]) / 2))
        confidence, classes = x[4], x[5]

        if classes != 4:
            cv2.circle(img, center, 10, (255, 255, 255), 5)
            cv2.putText(img, f"{DECODER_DICT[classes]} {confidence:.2f}", (center[0] + 5, center[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2, cv2.LINE_AA)
    

    cv2.imshow("i", img)
    if cv2.waitKey(1) == ord('q'):
        break


cv2.destroyAllWindows()

from util import *
from yolov5.load_model import YoloModel

import os
import cv2
import time
import torch
import numpy as np
import tensorflow as tf
from collections import deque

ct = 0
ptr_circle = []

def mousePoints(event, x, y, flags, params):
    global ct
    if event == cv2.EVENT_LBUTTONDOWN:
        if ct == 20:
            return False
        ptr_circle.append((x, y))
        ct += 1
        print(ptr_circle)

def center_crop(img, dim):
	width, height = img.shape[1], img.shape[0]

	# process crop width and height for max available dimension
	crop_width = dim[0] if dim[0] < img.shape[1] else img.shape[1]
	crop_height = dim[1] if dim[1] < img.shape[0] else img.shape[0] 
	mid_x, mid_y = int(width/2), int(height/2)
	cw2, ch2 = int(crop_width/2), int(crop_height/2) 
	crop_img = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
	return crop_img

def get_ball_img(img, center, radius=25):
    while 1:
        try:
            j, i = center
            rst = img[i - radius:i + radius, j - radius:j + radius]
            rst = cv2.resize(rst, (75, 75))
            break
        except:
            radius -= 1
        
    return cv2.cvtColor(rst, cv2.COLOR_BGR2RGB)


def crop_rails(ball_mask):
    ball_mask[0:43, :] = np.zeros((43, ball_mask.shape[1]))
    ball_mask[-35:, :] = np.zeros((35, ball_mask.shape[1]))
    ball_mask[:, 0:42] = np.zeros((ball_mask.shape[0], 42))
    ball_mask[:, -80:] = np.zeros((ball_mask.shape[0], 80))
    return ball_mask

def main():
    read_from_recording = True
    save_img = False
    select_ptr = False

    solids_count_queue = deque(maxlen=10)
    strips_count_queue = deque(maxlen=10)
    cue_ball_count_queue = deque(maxlen=5)
    prev_solids_count = None
    prev_strips_count = None

    prev_cue_ball = None
    curr_cue_ball = None
    cue_ball_changed = False
    curr_player = None

    prev_frame_time = 0
    new_frame_time = 0

    yolo_model = YoloModel().model
    yolo_model.iou = 0.3
    yolo_model.conf = 0.2
    yolo_model.max_det = 20
    
    if read_from_recording:
        img_ct = 210
        src = "data\\game_play"
        files_list = os.listdir(src)
    else:
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while 1:
        if read_from_recording:
            img_path = os.path.join(src, files_list[img_ct])
            if img_path[-3:] != "jpg":
                continue
            img = cv2.imread(img_path)
            img_ct += 1
        else:
            _, img = capture.read()

        if save_img:
            src = "data\\game_play"
            cv2.imwrite(src + f"\\{time.time()}.jpg", img)

        # find diamonds and warp image
        homo, _ = cv2.findHomography(np.array(REAL_DIAMONDS), np.array(DIAMONDS), cv2.RANSAC)
        img = cv2.warpPerspective(img, homo, np.array([WIDTH * ZOOM_MULTIPLIER, HEIGHT * ZOOM_MULTIPLIER]).astype(int))

        # apply yolo to locate balls and cue
        results = yolo_model(img, size=img.shape[1])
        results.render()
        rects = results.xyxy[0].cpu().numpy()
        if rects.shape[0] != 0:
            centers = remove_duplicate_points(np.apply_along_axis(get_center_from_pred, 1, rects))
        
        cue_ball_info = rects[rects[:, 5] == 3]
        cue_ball_center = None if len(cue_ball_info) == 0 else get_center_from_pred(cue_ball_info[0])

        solids_count_queue.append(rects[rects[:, 5] == 0].shape[0])
        strips_count_queue.append(rects[rects[:, 5] == 1].shape[0])
        solids_count = np.mean(solids_count_queue).astype(int)
        strips_count = np.mean(strips_count_queue).astype(int)
        
        cue_center = None
        if cue_ball_center is not None:
            # detect cue ball movements
            cue_ball_count_queue.append(cue_ball_center)
            curr_cue_ball = find_center_point_in_points(np.array(cue_ball_count_queue))
            if prev_cue_ball is not None and (changed := np.array_equal(prev_cue_ball, curr_cue_ball)) and not cue_ball_changed:
                cue_ball_changed = True
                if solids_count != prev_solids_count:
                    curr_player = "solids"
                elif strips_count != prev_strips_count:
                    curr_player = "strips"
                else:
                    curr_player = "solids" if curr_player == "strips" else "strips"

            elif prev_cue_ball is not None and not changed:
                cue_ball_changed = False
            prev_cue_ball = curr_cue_ball

            rects = rects[np.any((rects[:, :4] != cue_ball_info[0, :4]), axis=1)]
            cue_info = rects[rects[:, 5] == 4]
            if len(cue_info) != 0:
                cue_centers = np.apply_along_axis(get_center_from_pred, 1, cue_info)
                cue_center = find_center_point_in_points(cue_centers)

        if cue_ball_center is not None and cue_center is not None:
            # cue ball locator
            cv2.circle(img, cue_ball_center, 20, YELLOW, 3)

            # calculate aiming line
            end_pt = extend_line_to(cue_center, cue_ball_center)

            intersection = None
            intersections = []
            ball_idx = []
            for idx, ball in enumerate(centers):
                if distance_between_two_points(ball, cue_ball_center) < 10:
                    continue

                i = circle_line_intersection(cue_ball_center, ball, end_pt, radius=20)
                if i is not None:
                    intersections.append(i)
                    ball_idx.append(idx)
                
                if curr_player == "solids" and rects[idx, 5] == 0:
                    closest_pocket = closest_node(ball, POCKET_LOCATION)
                    print(ball, closest_pocket)

            if len(intersections) != 0:
                i = closest_node(cue_ball_center, intersections, return_index=True)
                intersection = intersections[i]
                ball = centers[ball_idx[i]]
                end_pt = extend_line_to(intersection, ball)

                # aiming line
                aiming_lines = bounce(intersection, end_pt, degrees=2)
                if aiming_lines is not None:
                    cv2.line(img, intersection, aiming_lines[0, :], BLACK, 2)
                    for i in range(aiming_lines.shape[0] - 1):
                        pt1, pt2 = aiming_lines[i, :], aiming_lines[i + 1, :]
                        cv2.line(img, pt2, pt1, BLACK, 2)
                else:
                    print("not a")
                    cv2.line(img, intersection, end_pt, BLACK, 2)

                # imaginary hit point
                cv2.circle(img, intersection, 2, YELLOW, -1)

                # imaginary circle + line
                cv2.circle(img, intersection, 10, BLUE, 1)
                cv2.line(img, cue_ball_center, intersection, WHITE, 2)

            else:
                # aiming line
                end_pts = bounce(cue_ball_center, end_pt, degrees=1)
                if end_pts is not None:
                    cv2.line(img, cue_ball_center, end_pts[0, :], WHITE, 2)
                    for i in range(end_pts.shape[0] - 1):
                        pt1, pt2 = end_pts[i, :], end_pts[i + 1, :]
                        cv2.line(img, pt2, pt1, WHITE, 2)

            # cue tip
            cv2.circle(img, cue_center, 3, BLACK, 3)

        # display current player
        cv2.putText(img, f"Current player is: {curr_player}", (300, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, BLUE, 2, cv2.LINE_AA)

        # draw rails and pockets
        cv2.rectangle(img, (RAIL_LOCATION[0], RAIL_LOCATION[2]), (RAIL_LOCATION[1], RAIL_LOCATION[3]), BLACK, 1)
        for x in np.array(POCKET_LOCATION).astype(int):
            cv2.circle(img, x, POCKET_RADIUS, BLUE, 5)
        
        # update previous value
        prev_cue_ball = curr_cue_ball
        prev_solids_count = solids_count
        prev_strips_count = strips_count
        
        # FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        cv2.putText(img, str(round(fps, 2)), (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, WHITE, 3, cv2.LINE_AA)

        cv2.imshow("img", img)
        if select_ptr:
            cv2.setMouseCallback("img", mousePoints)
            for x in ptr_circle:
                # x = x.astype(int)
                cv2.circle(img, x, 3, GREEN, 5)

        if cv2.waitKey(1) == ord('q'):
            break
    
    if not read_from_recording:
        capture.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

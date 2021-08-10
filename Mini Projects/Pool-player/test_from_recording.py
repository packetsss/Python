from util import *
from yolov5.load_model import YoloModel

import os
import cv2
import numpy as np

def main():
    src = "data\\yolo\\play"
    files_list = os.listdir(src)

    model = YoloModel().model
    model.iou = 0.2
    model.conf = 0.1
    model.max_det = 20

    for kk, file in enumerate(files_list[::5]):
        if kk < 2380:
            continue

        img_path = os.path.join(src, file)
        if img_path[-3:] != "jpg":
            continue

        img = cv2.imread(img_path)
        
        result = model(np.copy(img), size=700)
        rects = result.xyxy[0].cpu().numpy()
        centers = remove_duplicate_points(np.apply_along_axis(get_center_from_pred, 1, rects))
        
        cue_ball_info = rects[rects[:, 5] == 3]
        cue_ball_center = None if len(cue_ball_info) == 0 else get_center_from_pred(cue_ball_info[0])

        cue_info = rects[rects[:, 5] == 4]
        cue_center = None if len(cue_info) == 0 else get_center_from_pred(cue_info[0])
        '''
        Find cue using cv2

        cue_mask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), CUE_MASK[0], CUE_MASK[1])[:, :-23]
        cue_canny = cv2.GaussianBlur(cv2.Canny(cue_mask, 60, 60), (5, 5), cv2.BORDER_DEFAULT)
        lines = cv2.HoughLinesP(cue_canny, 1, np.pi/180, threshold=90, minLineLength=25, maxLineGap=5)

        start, end = None, None
        if lines is not None:
            m = max(lines, key=lambda l: distance_between_two_points(np.array([l[0][0], l[0][1]]), np.array([l[0][2], l[0][3]])))
            
            if point_in_rectangle(np.array([m[0][0], m[0][1]]), RAIL_LOCATION) or \
                point_in_rectangle(np.array([m[0][2], m[0][3]]), RAIL_LOCATION):
                ss, ee = np.array([m[0][0], m[0][1]]), np.array([m[0][2], m[0][3]])
            else:
                m = None
            
            pt1, pt2 = np.array([]), np.array([])
            for line in lines:
                x1, y1, x2, y2 = line[0]
                s, e = np.array([x1, y1]), np.array([x2, y2])

                slope = (y2 - y1) / (x2 - x1 + 1e-6)
                if -0.1 < slope < 0.1 and not point_in_rectangle(s, RAIL_LOCATION) and not point_in_rectangle(e, RAIL_LOCATION):
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

            if len(intersections) != 0:
                i = closest_node(cue_ball_center, intersections, return_index=True)
                intersection = intersections[i]
                ball = centers[ball_idx[i]]

                end_pt = extend_line_to(intersection, ball)

                a = bounce(intersection, end_pt, degrees=2)
                if a is not None:
                    pt1, pt2, pt3 = np.array(a).astype(int)
                    cv2.line(img, intersection, pt1, BLACK, 2)
                    cv2.line(img, pt2, pt1, BLACK, 2)
                    cv2.line(img, pt2, pt3, BLACK, 2)
                    
                # aiming line
                else:
                    cv2.line(img, intersection, end_pt, BLACK, 2)

                # imaginary hit point
                cv2.circle(img, intersection, 2, YELLOW, -1)

                # imaginary circle + line
                cv2.circle(img, intersection, 10, BLUE, 1)
                cv2.line(img, cue_ball_center, intersection, WHITE, 2)

                
            else:
                # aiming line
                cv2.line(img, cue_ball_center, end_pt, WHITE, 2)


            # cue tip
            if point_in_rectangle(cue_center, RAIL_LOCATION):
                cv2.circle(img, cue_center, 3, BLACK, 3)

        '''
        Plot every ball

        for x in rects:
            h, w = img.shape[:2]
            center = (int((x[0] + x[2]) / 2), int((x[1] + x[3]) / 2))
            confidence, classes = x[4], x[5]

            if classes < 4:
                # cv2.circle(img, center, 8, (255, 255, 255), 1)
                cv2.putText(img, f"{DECODER_DICT[classes]} {confidence:.2f}", (center[0] + 5, center[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2, cv2.LINE_AA)
        '''
        cv2.rectangle(img, (RAIL_LOCATION[0], RAIL_LOCATION[2]), (RAIL_LOCATION[1], RAIL_LOCATION[3]), BLACK, 1)
        cv2.imshow("i", img)
        if cv2.waitKey() == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

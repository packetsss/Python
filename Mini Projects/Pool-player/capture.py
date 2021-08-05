from utils import *

import os
import cv2
import time
import logging
import warnings
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

ct = 0
circle = np.zeros((4, 2), np.float32)

def mousePoints(event, x, y, flags, params):
    global ct
    if event == cv2.EVENT_LBUTTONDOWN:
        if ct == 4:
            return False
        circle[ct] = [x, y]
        ct += 1
        print(x, y)

def center_crop(img, dim):
	width, height = img.shape[1], img.shape[0]

	# process crop width and height for max available dimension
	crop_width = dim[0] if dim[0] < img.shape[1] else img.shape[1]
	crop_height = dim[1] if dim[1] < img.shape[0] else img.shape[0] 
	mid_x, mid_y = int(width/2), int(height/2)
	cw2, ch2 = int(crop_width/2), int(crop_height/2) 
	crop_img = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
	return crop_img

def get_ball_img(img, center):
    radius = 25
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
    wrap = True
    labels = None
    select_ptr = False
    last_img = None
    cue_ball_pos = None
    display_score = 10e10
    display_threshold = 1
    ball_list = []

    model = Model()
    model.load("models/ball.ckpt")
    
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while 1:
        _, img = capture.read()

        # transform image
        height, width = img.shape[:2]
        img = img[130:height-40, 60:width-230]

        # wrap to table
        if wrap:
            width, height = 900, 450

            pt1 = np.float32([[32, 11], [1594, 32], [9, 897], [1607, 867]])
            pt2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2) # use circle in 1st arg
            img = cv2.warpPerspective(img, matrix, (width, height))

        image_filter(img)
        
        gray = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (35, 35), 0)
        if last_img is not None:
            display_score = cv2.absdiff(gray, last_img).sum() / 210000
        last_img = gray

        # update ball labels
        if display_score > display_threshold:
            ball_mask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), BALL_MASK[0], BALL_MASK[1])
            ball_mask_2 = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), BALL_MASK_2[0], BALL_MASK_2[1])
            ball_mask_3 = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), BALL_MASK_3[0], BALL_MASK_3[1])
            ball_mask = crop_rails(ball_mask - ball_mask_2 - (255 - ball_mask_3))

            ball_canny = cv2.GaussianBlur(cv2.Canny(ball_mask, 60, 60), (5, 5), cv2.BORDER_DEFAULT)
            circles = cv2.HoughCircles(ball_canny, cv2.HOUGH_GRADIENT, 1.1, 12, param1=15, param2=15, minRadius=7, maxRadius=10)

            cropped_canny = ball_canny[45:-45, 50:-85]
            lines = cv2.HoughLinesP(cropped_canny, 1, np.pi/180, threshold=60, minLineLength=5, maxLineGap=5)
            
            if circles is not None:
                ball_list = []
                circles = np.uint16(np.around(circles))

                image_batch = tf.stack([get_ball_img(img, c[:2]) for c in circles[0, :]])
                labels = model.predict(image_batch, expand_img=False)

                for c, ball_label, ball_image in zip(circles[0, :], labels, image_batch):
                    center = c[:2]
                    ball_label = DECODER_DICT[np.argmax(ball_label)]
                    ball_list.append(Ball(center, ball_label, ball_image))

            print("Updated")
                
        # draw labels
        if len(ball_list) > 0:
            for i in range(len(ball_list)):
                ball = ball_list[i]

                if ball.label == "Cue-Ball":
                    cue_ball_pos = ball.center

                cv2.putText(img, ball.label, (ball.center[0] + 5, ball.center[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2, cv2.LINE_AA)
                cv2.circle(img, ball.center, 9, GREEN, 2)
        
        max_length = 0
        start = None
        end = None
        if lines is not None:
            display_threshold = 0.9
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)
                if length > max_length:
                    max_length = length
                    start, end = (x1 + 50, y1 + 45), (x2 + 50, y2 + 45)
            cv2.line(img, start, end, MAGENTA, 5)

            # find tip
            if cue_ball_pos is not None:
                find_distance_to_cue_ball = lambda pt: np.linalg.norm(np.array(pt) - np.array(cue_ball_pos))
                tip = min([start, end], key=find_distance_to_cue_ball)
                cv2.circle(img, tip, 5, CYAN, 2)

                cv2.line(img, tip, cue_ball_pos, MAGENTA, 2)
        else:
            display_threshold = 0.9

        cv2.imshow("img", img)
        cv2.imshow("canny", cv2.resize(cropped_canny, (0, 0), fx=0.5, fy=0.5))
        if select_ptr:
            cv2.setMouseCallback("img", mousePoints)
        if cv2.waitKey(1) == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

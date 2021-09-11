# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import cv2
import time
import numpy as np
import mediapipe as mp
import pyautogui

class PoseDetect:
    def __init__(self, mode=False, upBody=False, smooth=True, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detection_con = detection_con
        self.track_con = track_con
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()

    def find_pose(self, img, draw=True):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.rst = self.pose.process(img).pose_landmarks

        if self.rst is not None:
            if draw:
                self.mp_draw.draw_landmarks(img, self.rst, self.mp_pose.POSE_CONNECTIONS)
        
        return img

    def find_position(self, img, draw=True):
        lm_list = []

        if self.rst is not None:
            for i, landmark in enumerate(self.rst.landmark):
                # print(i, landmark) # 21 coord info
                h, w, ch = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h) # all 21 values

                lm_list.append((i, cx, cy))
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), 15, cv2.FILLED)

        return lm_list



def main():
    det = PoseDetect()

    prev_time = 0
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Live", 1300, 700)

    while 1:
        screenshot = pyautogui.screenshot()
        img = np.array(screenshot)

        img = det.find_pose(img)
        lst = det.find_position(img, draw=False)

        curr_time = time.time()
        fps = 1/(curr_time - prev_time)
        cv2.putText(img, str(int(fps)), (70, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 3)
        prev_time = curr_time
        cv2.imshow('Live', img)
        if cv2.waitKey(1) == ord('q'):
            break



if __name__ == '__main__':
    main()
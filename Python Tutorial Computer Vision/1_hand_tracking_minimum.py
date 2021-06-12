import cv2
import mediapipe as mp
import time


class HandDetect():
    def __init__(self, mode=False, max_hands=2, min_detection_conf=0.5, min_tracking_conf=0.5):
        self.mode, self.max_hands, self.min_detection_conf, self.min_tracking_conf = \
            mode, max_hands, min_detection_conf, min_tracking_conf
        

        
        self.mpHands = mp.solutions.hands.Hands(self.mode, self.max_hands, self.min_detection_conf, self.min_tracking_conf)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rst = self.mpHands.process(rgb)
        if (hands := rst.multi_hand_landmarks) is not None:
            for hand in hands:
                # for i, landmark in enumerate(hand.landmark):
                #     # print(i, landmark) # 21 coord info
                #     h, w, ch = img.shape
                #     cx, cy = int(landmark.x * w), int(landmark.y * h) # all 21 values

                #     if i == 0:
                #         cv2.circle(img, (cx, cy), 5, (255, 0, 255), 15, cv2.FILLED)
                if draw:
                    self.mpDraw.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)
    
    def find_pos(self, img):
        pass

def main():
    det = HandDetect()

    cap = cv2.VideoCapture(1)
    prev_time, curr_time = 0, 0

    while 1:
        success, img = cap.read()
        det.find_hands(img)
        

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Img", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
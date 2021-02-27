import cv2
from PIL import Image
import time
import numpy as np

class CVProceessing:
    def __init__(self):
        self.green_lower = (50, 130, 40)
        self.green_upper = (75, 255, 255)
        self.running = True
        self.img_arr = None
        self.processed_img=None

    def run_threaded(self, *args):
        img_arr = args[0]
        self.img_arr = img_arr
        # cv2.imshow('frame', mask)
        return self.processed_img

    def update(self):
        while self.running:
            if self.img_arr is not None:
                img_hsv = cv2.cvtColor(self.img_arr, cv2.COLOR_RGB2HSV)
                mask = cv2.inRange(img_hsv, self.green_lower, self.green_upper)
                mask_canny = cv2.Canny(self.img_arr, 100, 255)
                zero_channel = np.zeros((120, 160), dtype=np.uint8)
                self.processed_img = cv2.merge((zero_channel, mask, mask_canny), 3)
                # cv2.imwrite('mask.png', mask)
                time.sleep(0.005)

    def shutdown(self):
        self.running = False


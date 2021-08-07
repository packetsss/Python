import cv2
import numpy as np

class Ball:
    def __init__(self, center, label, image, radius=9):
        self.center = center
        self.label = label
        self.image = image
        self.radius = radius
    
    def get_bounding_box(self):
        x, y = self.center
        left, top = x - 2 * self.radius, y - 2 * self.radius
        right, bottom = x + 2 * self.radius, y + 2 * self.radius
        return top, bottom, left, right


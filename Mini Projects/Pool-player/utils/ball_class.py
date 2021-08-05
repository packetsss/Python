import cv2
import numpy as np

class Ball:
    def __init__(self, center, label, image, radius=9):
        self.center = center
        self.label = label
        self.image = image
        self.radius = radius

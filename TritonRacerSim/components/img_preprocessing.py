import time
from copy import copy
import cv2
import numpy as np
from PIL import Image

from TritonRacerSim.components.component import Component


class ImgPreprocessing(Component):
    def __init__(self, cfg={}):
        super().__init__(inputs=['cam/img'], outputs=['cam/processed_img'], threaded=True)
        self.running = True
        self.to_process_img = None
        self.processed_img = None
        self.cfg = cfg

    def step(self, *args):
        img_arr = args[0]
        self.to_process_img = copy(img_arr) if img_arr is not None else None
        return self.processed_img,

    def thread_step(self):
        while (self.running):
            while self.to_process_img is None:  # Waiting for new image
                time.sleep(0.005)

            # Copy the image, in case a new one is coming in
            img = self.to_process_img.copy()
            self.to_process_img = None
            img = self.__process(img)
            self.processed_img = img
            if self.cfg['preprocessing_preview_enabled']:
                cv2.imshow("Img Preprocessing", cv2.cvtColor(self.processed_img, cv2.COLOR_RGB2BGR))
                cv2.waitKey(1)

    def __process(self, img):
        # print(img.shape)
        layers = []
        merge_instruction = []

        img = self.__trim_brightness_contrast(img)
        if self.cfg['preprocessing_color_filter_enabled']:
            color_filtered_layers = self.__color_filter(img)
            # print(img.shape)
            layers.extend(color_filtered_layers)
            merge_instruction.extend(self.cfg['preprocessing_color_filter_destination_channels'])
        if self.cfg['preprocessing_edge_detection_enabled']:
            edge_filtered_layer = self.__edge_detection(img)
            layers.append(edge_filtered_layer)
            merge_instruction.append(self.cfg['preprocessing_edge_detection_destination_channel'])

        self.__merge(merge_instruction, img, layers)
        return img

    def __merge(self, instructions=[], destination=None, new_layers=None):
        # Replace the layers in destination according to instruction, preserving the untouched layers in the destination
        assert len(new_layers) == len(instructions)
        # print(destination.shape)
        for layer, instruction in zip(new_layers, instructions):
            destination[:, :, instruction] = layer
        # print(destination.shape)

    def __color_filter(self, img):
        hsv_img = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2HSV)
        bounds = self.cfg['preprocessing_color_filter_hsvs']
        output_layers = []

        for bound in bounds:
            mask = cv2.inRange(hsv_img, tuple(bound[0]), tuple(bound[1]))
            output_layers.append(mask)

        return output_layers

    def __edge_detection(self, img):
        threshold_a = self.cfg['preprocessing_edge_detection_threshold_a']
        threshold_b = self.cfg['preprocessing_edge_detection_threshold_b']
        return cv2.Canny(img, threshold_a, threshold_b)

    def __trim_brightness_contrast(self, img):
        # mean = cv2.mean(img[40:119,:,:])
        # multiplier = target_brightness / sum(list(mean))
        contrast = self.cfg['preprocessing_contrast_enhancement_ratio']
        offset = self.cfg['preprocessing_contrast_enhancement_offset']
        brightness_baseline = self.cfg['preprocessing_brightness_baseline']

        current_brightness = sum(list(cv2.mean(img[40:119, :, :])))
        delta = (brightness_baseline - current_brightness) / 3

        img_arr = img.astype(np.float32)
        if self.cfg['preprocessing_dynamic_brightness_enabled']:
            img_arr += delta
        img_arr -= offset
        img_arr *= contrast
        img_arr += offset
        img_arr = np.clip(img_arr, 0, 255)
        img = img_arr.astype(np.uint8)
        # print(f'{sum(list(mean))}\r', end="")
        # print(sum(list(cv2.mean(cv2.absdiff(img, new_img)))))
        return img

    def onShutdown(self):
        self.running = False

    def getName(self):
        return 'Image Preprocessing'

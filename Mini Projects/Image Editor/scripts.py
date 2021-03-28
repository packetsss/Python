import numpy as np
import cv2
from scipy import ndimage
import math
from copy import deepcopy


class Images:
    def __init__(self, img):
        self.img = cv2.imread(img, 1)
        if self.img.shape[0] / self.img.shape[1] < 0.76:
            self.img_width = 1100
            self.img_height = int(self.img_width * self.img.shape[0] / self.img.shape[1])
        else:
            self.img_height = 700
            self.img_width = int(self.img_height * self.img.shape[1] / self.img.shape[0])

        self.img = cv2.resize(self.img, (self.img_width, self.img_height))
        self.img_copy = deepcopy(self.img)
        self.grand_img_copy = deepcopy(self.img)

        self.img_name = img.split('\\')[-1].split(".")[0]
        self.img_format = img.split('\\')[-1].split(".")[1]

        self.left, self.right, self.top, self.bottom = None, None, None, None

        # self.bypass_censorship()

    def auto_contrast(self):
        clip_hist_percent = 20
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_size = len(hist)
        accumulator = [float(hist[0])]
        for index in range(1, hist_size):
            accumulator.append(accumulator[index - 1] + float(hist[index]))
        maximum = accumulator[-1]
        clip_hist_percent *= (maximum / 100.0)
        clip_hist_percent /= 2.0
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1
        maximum_gray = hist_size - 1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha

        self.img = cv2.convertScaleAbs(self.img, alpha=alpha, beta=beta)

    def auto_sharpen(self):
        self.img = cv2.detailEnhance(self.img, sigma_s=10, sigma_r=0.3)

    def auto_cartoon(self, style=0):
        edges1 = cv2.bitwise_not(cv2.Canny(self.img, 100, 200))
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 7)
        dst = cv2.edgePreservingFilter(self.img, flags=2, sigma_s=64, sigma_r=0.25)

        if not style:
            # less blurry
            self.img = cv2.bitwise_and(dst, dst, mask=edges1)
        else:
            # more blurry
            self.img = cv2.bitwise_and(dst, dst, mask=edges2)

    def auto_invert(self):
        self.img = cv2.bitwise_not(self.img)

    def change_b_c(self, alpha=1, beta=0):
        # contrast from 0 to 3, brightness from -100 to 100
        self.img = cv2.convertScaleAbs(self.img, alpha=alpha, beta=beta)

    def change_saturation(self, value):
        # -300 to 300
        img_hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv2.split(img_hsv)
        s += value
        s = np.clip(s, 0, 255)
        img_hsv = cv2.merge([h, s, v])
        self.img = cv2.cvtColor(img_hsv.astype("uint8"), cv2.COLOR_HSV2BGR)

    def remove_color(self, color):
        h = color.lstrip('#')
        color = np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)])

        img_hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV).astype("float32")
        low = np.array([color[0] - 15, 0, 20])
        high = np.array([color[0] + 15, 255, 255])
        mask = cv2.inRange(img_hsv, low, high)
        img_hsv[mask > 0] = (0, 0, 255)
        self.img = cv2.cvtColor(img_hsv.astype("uint8"), cv2.COLOR_HSV2BGR)

    def crop_img(self, left, right, top, bottom):
        self.img = self.img[left:right, top:bottom]

    def rotate_img(self, angle, crop=False, flip=[False, False]):
        self.reset(flip)
        if not crop:
            self.img = cv2.resize(self.img, (0, 0), fx=0.5, fy=0.5)
            w, h = self.img.shape[1], self.img.shape[0]
        else:
            w, h = self.img_width, self.img_height

        self.img = ndimage.rotate(self.img, angle)

        angle = math.radians(angle)
        quadrant = int(math.floor(angle / (math.pi / 2))) & 3
        sign_alpha = angle if ((quadrant & 1) == 0) else math.pi - angle
        alpha = (sign_alpha % math.pi + math.pi) % math.pi
        bb_w = w * math.cos(alpha) + h * math.sin(alpha)
        bb_h = w * math.sin(alpha) + h * math.cos(alpha)
        gamma = math.atan2(bb_w, bb_w) if (w < h) else math.atan2(bb_w, bb_w)
        delta = math.pi - alpha - gamma
        length = h if (w < h) else w
        d = length * math.cos(alpha)
        a = d * math.sin(alpha) / math.sin(delta)
        y = a * math.cos(gamma)
        x = y * math.tan(gamma)
        wr, hr = bb_w - 2 * x, bb_h - 2 * y

        midpoint = (np.array(self.img.shape[:-1]) // 2)[::-1]
        half_w, half_h = wr // 2, hr // 2
        self.left, self.right, self.top, self.bottom = int(midpoint[0] - half_w), int(midpoint[0] + half_w), \
                                                       int(midpoint[1] - half_h), int(midpoint[1] + half_h)

    def detect_face(self):
        face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')
        # eye_cascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')

        gray_scale_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        face_coord = face_cascade.detectMultiScale(gray_scale_img)

        return face_coord

    def bypass_censorship(self):
        smaller_img = cv2.resize(self.img, (0, 0), fx=0.5, fy=0.5)
        image = np.zeros(self.img.shape, np.uint8)

        width = self.img.shape[1]
        height = self.img.shape[0]
        image[:height // 2, :width // 2] = cv2.rotate(smaller_img, cv2.cv2.ROTATE_180)
        image[height // 2:, :width // 2] = smaller_img
        image[height // 2:, width // 2:] = cv2.rotate(smaller_img, cv2.cv2.ROTATE_180)
        image[:height // 2, width // 2:] = smaller_img
        self.img = image

    def save_img(self, file):
        cv2.imwrite(file, self.img)

    def reset(self, flip=[False, False]):
        self.img = deepcopy(self.img_copy)
        if flip[0]:
            self.img = cv2.flip(self.img, 0)
        if flip[1]:
            self.img = cv2.flip(self.img, 1)

    def grand_reset(self):
        self.img = deepcopy(self.grand_img_copy)
        self.img_copy = deepcopy(self.grand_img_copy)


def main():
    path = "ppl.jpg"
    img = Images(path)
    img_name = path.split('\\')[-1].split(".")[0]

    cv2.imshow(img_name, img.img)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

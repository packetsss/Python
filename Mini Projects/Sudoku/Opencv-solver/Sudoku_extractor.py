import asyncio
import operator
import threading

import cv2
import numpy as np
import pytesseract
from Sudoku_solver import solve


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped

class Extract:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype="int64")
        self.solved = False

    @staticmethod
    def convert_when_colour(color, img):
        """Dynamically converts an image to colour if the input colour is a tuple and the image is grayscale."""
        if len(color) == 3:
            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            elif img.shape[2] == 1:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img

    @staticmethod
    def pre_process_image(img, skip_dilate=False):
        """Uses a blurring function, adaptive thresholding and dilation to expose the main features of an image."""

        # Gaussian blur with a kernal size (height, width) of 9.
        # Note that kernal sizes must be positive and odd and the kernel must be square.
        proc = cv2.GaussianBlur(img.copy(), (9, 9), 0)

        # Adaptive threshold using 11 nearest neighbour pixels
        proc = cv2.adaptiveThreshold(proc, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Invert colours, so gridlines have non-zero pixel values.
        # Necessary to dilate the image, otherwise will look like erosion instead.
        proc = cv2.bitwise_not(proc, proc)

        if not skip_dilate:
            # Dilate the image to increase the size of the grid lines.
            kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
            proc = cv2.dilate(proc, kernel)

        return proc

    @staticmethod
    def find_corners_of_largest_polygon(img):
        """Finds the 4 extreme corners of the largest contour in the image."""
        contours, h = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
        contours = sorted(contours, key=cv2.contourArea, reverse=True)  # Sort by area, descending
        polygon = contours[0]  # Largest image

        # Use of `operator.itemgetter` with `max` and `min` allows us to get the index of the point Each point is an
        # array of 1 coordinate, hence the [0] getter, then [0] or [1] used to get x and y respectively.

        # Bottom-right point has the largest (x + y) value
        # Top-left has point smallest (x + y) value
        # Bottom-left point has smallest (x - y) value
        # Top-right point has largest (x - y) value
        bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
        top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
        bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
        top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))

        # Return an array of all 4 points using the indices
        # Each point is in its own array of one coordinate
        return [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]

    @staticmethod
    def distance_between(p1, p2):
        """Returns the scalar distance between two points"""
        a = p2[0] - p1[0]
        b = p2[1] - p1[1]
        return np.sqrt((a ** 2) + (b ** 2))

    def crop_and_warp(self, img, crop_rect):
        """Crops and warps a rectangular section from an image into a square of similar size."""

        # Rectangle described by top left, top right, bottom right and bottom left points
        top_left, top_right, bottom_right, bottom_left = crop_rect[0], crop_rect[1], crop_rect[2], crop_rect[3]

        # Explicitly set the data type to float32 or `getPerspectiveTransform` will throw an error
        src = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')

        # Get the longest side in the rectangle
        side = max([
            self.distance_between(bottom_right, top_right),
            self.distance_between(top_left, bottom_left),
            self.distance_between(bottom_right, bottom_left),
            self.distance_between(top_left, top_right)
        ])

        # Describe a square with side of the calculated length, this is the new perspective we want to warp to
        dst = np.array([[0, 0], [side - 1, 0], [side - 1, side - 1], [0, side - 1]], dtype='float32')

        # Gets the transformation matrix for skewing the image to fit a square by comparing the 4 before and after
        # points
        m = cv2.getPerspectiveTransform(src, dst)

        # Performs the transformation on the original image
        return cv2.warpPerspective(img, m, (int(side), int(side)))

    @staticmethod
    def infer_grid(img):
        """Infers 81 cell grid from a square image."""
        squares = []
        side = img.shape[:1]
        side = side[0] / 9

        # Note that we swap j and i here so the rectangles are stored in the list reading left-right instead of
        # top-down.
        for j in range(9):
            for i in range(9):
                p1 = (i * side, j * side)  # Top left corner of a bounding box
                p2 = ((i + 1) * side, (j + 1) * side)  # Bottom right corner of bounding box
                squares.append((p1, p2))
        return squares

    @staticmethod
    def cut_from_rect(img, rect):
        """Cuts a rectangle from an image using the top left and bottom right points."""
        return img[int(rect[0][1]):int(rect[1][1]), int(rect[0][0]):int(rect[1][0])]

    @staticmethod
    def scale_and_centre(img, size, margin=0, background=0):
        """Scales and centres an image onto a new background square."""
        h, w = img.shape[:2]

        def centre_pad(length):
            """Handles centering for a given length that may be odd or even."""
            if length % 2 == 0:
                side1 = int((size - length) / 2)
                side2 = side1
            else:
                side1 = int((size - length) / 2)
                side2 = side1 + 1
            return side1, side2

        def scale(r, x):
            return int(r * x)

        if h > w:
            t_pad = int(margin / 2)
            b_pad = t_pad
            ratio = (size - margin) / h
            w, h = scale(ratio, w), scale(ratio, h)
            l_pad, r_pad = centre_pad(w)
        else:
            l_pad = int(margin / 2)
            r_pad = l_pad
            ratio = (size - margin) / w
            w, h = scale(ratio, w), scale(ratio, h)
            t_pad, b_pad = centre_pad(h)

        img = cv2.resize(img, (w, h))
        img = cv2.copyMakeBorder(img, t_pad, b_pad, l_pad, r_pad, cv2.BORDER_CONSTANT, None, background)
        return cv2.resize(img, (size, size))


    def find_largest_feature(self, inp_img, scan_tl=None, scan_br=None, x_idx=None, y_idx=None):
        """
        Uses the fact the `floodFill` function returns a bounding box of the area it filled to find the biggest
        connected pixel structure in the image. Fills this structure in white, reducing the rest to black.
        """
        img = inp_img.copy()  # Copy the image, leaving the original untouched
        height, width = img.shape[:2]

        max_area = 0
        seed_point = (None, None)

        if scan_tl is None:
            scan_tl = [0, 0]

        if scan_br is None:
            scan_br = [width, height]

        # Loop through the image
        for x in range(scan_tl[0], scan_br[0]):
            for y in range(scan_tl[1], scan_br[1]):
                # Only operate on light or white squares
                if img.item(y,
                            x) == 255 and x < width and y < height:  # Note that .item() appears to take input as y, x

                    area = cv2.floodFill(img, None, (x, y), 64)
                    if area[0] > max_area:  # Gets the maximum bound area which should be the grid
                        max_area = area[0]
                        seed_point = (x, y)

        # Colour everything grey (compensates for features outside of our middle scanning range
        for x in range(width):
            for y in range(height):
                if img.item(y, x) == 255 and x < width and y < height:
                    cv2.floodFill(img, None, (x, y), 0)

        # Highlight the main feature
        if all([p is not None for p in seed_point]):
            mask = np.zeros((height + 2, width + 2), np.uint8)  # Mask that is 2 pixels bigger than the image
            cv2.floodFill(img, mask, seed_point, 255)

        # ---------------------------------------------------------------------------------
        num = pytesseract.image_to_string(img, lang='eng',
                                        config='--psm 10 --oem 1 -c tessedit_char_whitelist=0123456789')
        num = int(num[0]) if num[0] != "\x0c" else 0
        self.board[y_idx, x_idx] = num
        # plt.imshow(img)
        # plt.show()
        # ---------------------------------------------------------------------------------

    def extract_digit(self, img, rect, x, y):
        """Extracts a digit (if one exists) from a Sudoku square."""

        digit = self.cut_from_rect(img, rect)  # Get the digit box from the whole square
        # plt.imshow(digit)
        # plt.show()

        # Use fill feature finding to get the largest feature in middle of the box
        # Margin used to define an area in the middle we would expect to find a pixel belonging to the digit
        h, w = digit.shape[:2]
        margin = int(np.mean([h, w]) / 2.5)
        self.find_largest_feature(digit, [margin, margin], [w - margin, h - margin], x, y)

    # @background
    def get_board(self, img, squares):
        """Extracts digits from their cells and builds an array"""
        y_idx, x_idx = 0, 0

        img = self.pre_process_image(img.copy(), skip_dilate=True)
        for square in squares:
            self.extract_digit(img, square, x_idx, y_idx)
            # pool.submit(self.extract_digit, img, square, x_idx, y_idx)
            x_idx += 1
            if x_idx == 9:
                y_idx += 1
                x_idx = 0

        return self.board

    def waiter(self):
        while not self.solved:
            print("Solving in progress...", end="\r", flush=True)
        print("", end="\r", flush=True)

    def extract_sudoku(self, path):
        trd = threading.Thread(target=self.waiter, daemon=False)
        trd.start()
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        original = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        processed = self.pre_process_image(original)
        corners = self.find_corners_of_largest_polygon(processed)
        cropped = self.crop_and_warp(original, corners)
        squares = self.infer_grid(cropped)
        self.get_board(cropped, squares)
        self.solved = True
        return self.board


img = Extract()
board = img.extract_sudoku("src/board.jpg")
# board = list([list(l) for l in board])
try:
    board = solve(board).ai()
    print(board[0])
except Exception as e:
    print(e)


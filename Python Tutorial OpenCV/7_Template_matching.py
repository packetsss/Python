import cv2
import numpy as np

img = cv2.resize(cv2.imread('src/soccer_practice.jpg', 0), (0, 0), fx=0.7, fy=0.7)
ball = cv2.resize(cv2.imread('src/ball.png', 0), (0, 0), fx=0.7, fy=0.7)
shoe = cv2.resize(cv2.imread('src/shoe.png', 0), (0, 0), fx=0.7, fy=0.7)
h, w = ball.shape

methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
# try each method and use the best one

for method in methods:
    img2 = img.copy()
    ball_result = cv2.matchTemplate(img2, ball, method)
    shoe_result = cv2.matchTemplate(img2, shoe, method)
    # (W - w + 1, H - h + 1)
    # uppercase is img dimension, lowercase is result dimension
    # e.g.:
    '''
    [[255, 255, 255, 255],
     [255, 255, 255, 255],
     [255, 255, 255, 255],
     [255, 255, 255, 255]]
    
    [[255, 255],
     [255, 255]]
    
    return:
    [[1, 1, 1],
     [0, 0, 1],
     [1, 0, 0]]
     
    find the 1's in the output
    
    '''
    _, _, ball_min_loc, ball_max_loc = cv2.minMaxLoc(ball_result)
    _, _, shoe_min_loc, shoe_max_loc = cv2.minMaxLoc(shoe_result)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        ball_location = ball_min_loc
        shoe_location = shoe_min_loc
    else:
        ball_location = ball_max_loc
        shoe_location = shoe_max_loc

    ball_bottom_right = (ball_location[0] + w, ball_location[1] + h)
    shoe_bottom_right = (shoe_location[0] + w, shoe_location[1] + h)

    cv2.rectangle(img2, ball_location, ball_bottom_right, 255, 5)
    cv2.rectangle(img2, shoe_location, shoe_bottom_right, 255, 5)

    cv2.imshow("Image", img2)
    cv2.waitKey()
    cv2.destroyAllWindows()
    print(method)


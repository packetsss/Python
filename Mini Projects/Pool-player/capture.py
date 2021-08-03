import cv2
import numpy as np
from filter import image_filter

ct = 0
circle = np.zeros((4, 2), np.float32)
WHITE_BALL_MASK = ((94, 144, 76), (255, 255, 253))# ((78, 82, 68), (255, 255, 119))

def mousePoints(event, x, y, flags, params):
    global ct
    if event == cv2.EVENT_LBUTTONDOWN:
        if ct == 4:
            return False
        circle[ct] = [x, y]
        ct += 1
        print(x, y)

def center_crop(img, dim):
	"""Returns center cropped image
	Args:
	img: image to be center cropped
	dim: dimensions (width, height) to be cropped
	"""
	width, height = img.shape[1], img.shape[0]

	# process crop width and height for max available dimension
	crop_width = dim[0] if dim[0]<img.shape[1] else img.shape[1]
	crop_height = dim[1] if dim[1]<img.shape[0] else img.shape[0] 
	mid_x, mid_y = int(width/2), int(height/2)
	cw2, ch2 = int(crop_width/2), int(crop_height/2) 
	crop_img = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
	return crop_img

def scale_image(img, factor=1):
	"""Returns resize image by scale factor.
	This helps to retain resolution ratio while resizing.
	Args:
	img: image to be scaled
	factor: scale factor to resize
	"""
	return cv2.resize(img,(int(img.shape[1]*factor), int(img.shape[0]*factor)))

def main():
    wrap = True
    select_ptr = False
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while 1:
        _, img = capture.read()

        height, width = img.shape[:2]

        # transform image
        # img = scale_image(center_crop(img, (1900, 550)), factor=1.5)
        # img = cv2.resize(img, (0, 0), fx=0.5, fy=1)
        img = img[130:height-40, 60:width-230]

        if wrap:
            width, height = 900, 450

            pt1 = np.float32([[32, 11], [1594, 32], [9, 897], [1607, 867]])
            pt2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2) # use circle in 1st arg
            img = cv2.warpPerspective(img, matrix, (width, height))
            
            '''
            for i in range(4):
                cv2.circle(img, (int(circle[i][0]), int(circle[i][1])), 5, (0, 255, 0), cv2.FILLED)
            '''

        ball_mask = cv2.inRange(
            cv2.cvtColor(

                    img, #center_crop(img, (850, 400)), factor=1.5)
                cv2.COLOR_BGR2RGB), 
            WHITE_BALL_MASK[0], WHITE_BALL_MASK[1])
    
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        contours, hierarch = cv2.findContours(thresh, 1, 2)

        for cnt in contours:
            # (x, y), radius = cv2.minEnclosingCircle(cnt)
            # center = (int(x), int(y))
            # radius = int(radius)

            # cv2.circle(img, center, radius,(0, 255, 0), 3)
            # cv2.circle(img, center, 3, (255, 255, 0), 3)
            cv2.drawContours(img, [cnt], 0, (0, 0, 255), 3)
        
        blurred_mask =  cv2.medianBlur(ball_mask, 7)
        blurred_mask[0:43, :] = np.zeros((43, blurred_mask.shape[1]))
        blurred_mask[-35:, :] = np.zeros((35, blurred_mask.shape[1]))
        blurred_mask[:, 0:42] = np.zeros((blurred_mask.shape[0], 42))
        blurred_mask[:, -40:] = np.zeros((blurred_mask.shape[0], 40))

        # circles = cv2.HoughCircles(blurred_mask, cv2.HOUGH_GRADIENT, 1.3, 1, param1=15, param2=11, minRadius=0, maxRadius=20)
        # if circles is not None:
        #     circles = np.uint16(np.around(circles))
        #     for i in circles[0, :]:
        #         abs_dif = i[1]
        #         # draw the outer circle
        #         cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        #         # draw the center of the circle
        #         cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
        # image_filter(img)

        cv2.imshow("img", img)
        if select_ptr:
            cv2.setMouseCallback("img", mousePoints)
        if cv2.waitKey(1) == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

import cv2

trained_face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

img = cv2.imread("pto.jfif")

grayscaled_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_coord = trained_face_data.detectMultiScale(grayscaled_img)

cv2.rectangle(img, face_coord, (0, 255, 0), 5)


cv2.imshow("Face Detector", img)
cv2.waitKey()


import numpy as np
import cv2 as cv

# define field for the number of images captured
imagesCapturedNum = 0

# start video capture
videoCapture = cv.VideoCapture(0)
if not videoCapture.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = videoCapture.read()
    if not ret:
        print("Cannot receive frame")
        break
    cv.imshow(winname = "Capture", mat = frame)
    key = cv.waitKey(delay = 10)

    # quit with on q
    if key == ord("q"):
        break

    # capture frame on c
    if key == ord("c"):
        cv.imwrite(
            filename = "data\image{0}.png".format(imagesCapturedNum),
            img = frame
        )
        imagesCapturedNum += 1

        # end on the 10th image captured
        if imagesCapturedNum > 9:
            break

videoCapture.release()
cv.destroyAllWindows()
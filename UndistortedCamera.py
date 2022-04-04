import numpy as np
import cv2 as cv
import yaml

# load camera parameters [2]
with open("./data/cameraParameters.yaml") as file:
    cameraParameters = yaml.full_load(file)

cameraMatrix = np.zeros((3, 3), np.float32)
# focal length
cameraMatrix[0, 0] = cameraParameters["intrinsics"]["fx"]
cameraMatrix[1, 1] = cameraParameters["intrinsics"]["fy"]
# principal point
cameraMatrix[0, 2] = cameraParameters["intrinsics"]["cx"]
cameraMatrix[1, 2] = cameraParameters["intrinsics"]["cy"]
cameraMatrix[2, 2] = 1

distortionCoefficients = np.zeros((1, 5), np.float32)
# radial distortion coefficients
distortionCoefficients[0, 0] = cameraParameters["distortionCoefficients"]["k1"]
distortionCoefficients[0, 1] = cameraParameters["distortionCoefficients"]["k2"]
distortionCoefficients[0, 4] = cameraParameters["distortionCoefficients"]["k3"]
# tangential distortion coefficients
distortionCoefficients[0, 2] = cameraParameters["distortionCoefficients"]["p1"]
distortionCoefficients[0, 3] = cameraParameters["distortionCoefficients"]["p2"]

# start video capture and receive a first frame
videoCapture = cv.VideoCapture(0)
if not videoCapture.isOpened():
    print("Cannot open camera")
    exit()
ret, frame = videoCapture.read()
if not ret:
    print("Cannot receive frame")
    exit()

# calculate refined camera matrix to reduce the black/undefined 
# corners. Parameter alpha can be set from 0 to 1 and defines 
# how much of the black pixels should be visible [1]
newCameraMatrix, (x, y, width, height) = cv.getOptimalNewCameraMatrix(
    cameraMatrix = cameraMatrix, distCoeffs = distortionCoefficients,
    imageSize = frame.shape[:2], alpha = 0.5, newImgSize = frame.shape[:2]
)

while True:
    # undistort frame [1]
    frameUndistorted = cv.undistort(
        src = frame, cameraMatrix = cameraMatrix,
        distCoeffs = distortionCoefficients, dst = None,
        newCameraMatrix = newCameraMatrix
    )
    ret, frame = videoCapture.read()

    # display undistorted frame
    cv.imshow(winname = "UndistortedCamera", mat = frameUndistorted)

    # quit on 'q'
    if cv.waitKey(10) == ord("q"):
        break

videoCapture.release()
cv.destroyAllWindows()

# [1] https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html
# [2] https://pynative.com/python-yaml/#h-python-yaml-load-read-yaml-file
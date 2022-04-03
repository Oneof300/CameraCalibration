import numpy as np
import cv2 as cv
import yaml

# load camera parameters, reference:
# https://pynative.com/python-yaml/#h-python-yaml-load-read-yaml-file
with open("./data/cameraParameters.yaml") as file:
    cameraParameters = yaml.full_load(file)

cameraMatrix = np.zeros((3, 3), np.float32)
cameraMatrix[0, 0] = cameraParameters["intrinsics"]["fx"]
cameraMatrix[1, 1] = cameraParameters["intrinsics"]["fy"]
cameraMatrix[0, 2] = cameraParameters["intrinsics"]["cx"]
cameraMatrix[1, 2] = cameraParameters["intrinsics"]["cy"]
cameraMatrix[2, 2] = 1

distortionCoefficients = np.zeros((1, 5), np.float32)
distortionCoefficients[0, 0] = cameraParameters["distortionCoefficients"]["k1"]
distortionCoefficients[0, 1] = cameraParameters["distortionCoefficients"]["k2"]
distortionCoefficients[0, 2] = cameraParameters["distortionCoefficients"]["p1"]
distortionCoefficients[0, 3] = cameraParameters["distortionCoefficients"]["p2"]
distortionCoefficients[0, 4] = cameraParameters["distortionCoefficients"]["k3"]

# start video capture and receive a first frame
videoCapture = cv.VideoCapture(0)
if not videoCapture.isOpened():
    print("Cannot open camera")
    exit()
ret, frame = videoCapture.read()
if not ret:
    print("Cannot receive frame")
    exit()

# calculate new camera matrix
newCameraMatrix, (x, y, width, height) = cv.getOptimalNewCameraMatrix(
    cameraMatrix = cameraMatrix, distCoeffs = distortionCoefficients,
    imageSize = frame.shape[:2], alpha = 1, newImageSize = frame.shape[:2]
)

while True:
    # undistort frame
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
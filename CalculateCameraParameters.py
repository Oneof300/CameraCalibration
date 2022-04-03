import numpy as np
import cv2 as cv
import glob
import yaml

# load image names
imageFilenames = glob.glob("./data/*.png")

# define chessboard size and refined corners calculation criteria
chessboardSize = (7, 5)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# define points in world coordinates
worldPoints = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
worldPoints[:, :2] = np.mgrid[
    0:chessboardSize[0], 0:chessboardSize[1]
].T.reshape(-1, 2)

# define fields to store point data for all images
worldPointsPerImage = []
imagePointsPerImage = []

# calculate camera parameters
for imageFilename in imageFilenames:

    # read image
    image = cv.imread(filename = imageFilename)
    imageGray = cv.cvtColor(src = image, code = cv.COLOR_BGR2GRAY)

    # find chessboard corners as points in image coordinates
    ret, imagePoints = cv.findChessboardCorners(
        image = imageGray, patternSize = chessboardSize)

    if ret == True:
        # get more precise chessboard corners
        imagePointsRefined = cv.cornerSubPix(
            image = imageGray, corners = imagePoints, winSize = (11, 11),
            zeroZone = (-1, -1), criteria = criteria
        )

        # store point data
        worldPointsPerImage.append(worldPoints)
        imagePointsPerImage.append(imagePoints)

        # display found chessboard corners
        cv.drawChessboardCorners(
            image = image, patternSize = chessboardSize,
            corners = imagePointsRefined, patternWasFound = ret
        )
        cv.imshow("ChessboardCorners", image)
        cv.waitKey(delay = 500)

cv.destroyAllWindows()

# calculate camera calibration
ret, cameraMatrix, distortionCoefficients, rvecs, tvecs = cv.calibrateCamera(
    objectPoints = worldPointsPerImage, imagePoints = imagePointsPerImage,
    imageSize = imageGray.shape[::-1], cameraMatrix = None, distCoeffs = None
)

# store calibration, reference:
# https://pynative.com/python-yaml/#h-python-yaml-dump-write-into-yaml-file
cameraParameters = {
    "distortionCoefficients" : {
        "k1" : distortionCoefficients[0, 0].item(),
        "k2" : distortionCoefficients[0, 1].item(),
        "p1" : distortionCoefficients[0, 2].item(),
        "p2" : distortionCoefficients[0, 3].item(),
        "k3" : distortionCoefficients[0, 4].item()
    },
    "intrinsics" : {
        "fx" : cameraMatrix[0, 0].item(),
        "fy" : cameraMatrix[1, 1].item(),
        "cx" : cameraMatrix[0, 2].item(),
        "cy" : cameraMatrix[1, 2].item()
    }
}

with open("./data/cameraParameters.yaml", "w") as file:
    cameraParameters = yaml.dump(cameraParameters, file)
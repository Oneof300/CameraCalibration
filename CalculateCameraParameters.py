import numpy as np
import cv2 as cv
import glob
import yaml

# load image names [1]
imageFilenames = glob.glob("./data/*.png")

# define chessboard size and refined corners calculation criteria [1]
chessboardSize = (7, 5)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# define points in world coordinates [1]
worldPoints = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
worldPoints[:, :2] = np.mgrid[
    0:chessboardSize[0], 0:chessboardSize[1]
].T.reshape(-1, 2)

# define fields to store point data for all images [1]
worldPointsPerImage = []
imagePointsPerImage = []

# calculate camera parameters
for imageFilename in imageFilenames:

    # read image
    image = cv.imread(filename = imageFilename)
    imageGray = cv.cvtColor(src = image, code = cv.COLOR_BGR2GRAY)

    # find chessboard corners as points in image coordinates [1]
    ret, imagePoints = cv.findChessboardCorners(
        image = imageGray, patternSize = chessboardSize)

    if ret == True:
        # get more precise chessboard corners [1]
        imagePointsRefined = cv.cornerSubPix(
            image = imageGray, corners = imagePoints, winSize = (11, 11),
            zeroZone = (-1, -1), criteria = criteria
        )

        # store point data [1]
        worldPointsPerImage.append(worldPoints)
        imagePointsPerImage.append(imagePoints)

        # display found chessboard corners [1]
        cv.drawChessboardCorners(
            image = image, patternSize = chessboardSize,
            corners = imagePointsRefined, patternWasFound = ret
        )
        
        cv.imshow("ChessboardCorners", image)
        cv.waitKey(delay = 5)

cv.destroyAllWindows()

# calculate camera calibration [1]
ret, cameraMatrix, distortionCoefficients, rotationVectors, translationVectors = cv.calibrateCamera(
    objectPoints = worldPointsPerImage, imagePoints = imagePointsPerImage,
    imageSize = imageGray.shape[::-1], cameraMatrix = None, distCoeffs = None
)

# calculate reprojection error [1]
errorSum = 0
for i in range(len(worldPointsPerImage)):
    imagePointsProjected, jacobian = cv.projectPoints(
        objectPoints = worldPointsPerImage[i], rvec = rotationVectors[i], tvec = translationVectors[i],
        cameraMatrix = cameraMatrix, distCoeffs = distortionCoefficients
    )
    error = cv.norm(
        src1 = imagePointsPerImage[i], src2 = imagePointsProjected, normType = cv.NORM_L2
    ) / len(imagePointsProjected)
    errorSum += error

print("total reprojection error: {0}".format((errorSum / len(worldPointsPerImage))))

# store calibration [2]
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
    },
    "extrinsics" : []
}

# iterate through vectors to append them to the extrinsics
for i in range(len(worldPointsPerImage)):
    cameraParameters["extrinsics"].append({
        "r1" : rotationVectors[i][0, 0].item(),
        "r2" : rotationVectors[i][1, 0].item(),
        "r3" : rotationVectors[i][2, 0].item(),
        "t1" : translationVectors[i][0, 0].item(),
        "t2" : translationVectors[i][1, 0].item(),
        "t3" : translationVectors[i][2, 0].item()
    })

with open("./data/cameraParameters.yaml", "w") as file:
    cameraParameters = yaml.dump(cameraParameters, file)

# [1] https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html
# [2] https://pynative.com/python-yaml/#h-python-yaml-dump-write-into-yaml-file
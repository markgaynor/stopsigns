import cv2, time, imutils
import numpy as np
from matplotlib import pyplot as plt

def detect_mse(img):
    """ 
    Determines whether the input image contains a stop sign using an image pyramid, a sliding window and 
    a simple MSE comparison. 
    """
    # Reads the template image, converts it to grayscale and detects edges. 
    template = cv2.imread("img/templates/stop_sign_small.png")
    (tH, tW) = template.shape[:2]

    img = cv2.imread(img)
    found = None

    # loop over the scales of the image
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(img, width = int(img.shape[1] * scale))
            r = img.shape[1] / float(resized.shape[1])

            # if the resized image is smaller than the template, then break
            # from the loop
            if resized.shape[0] < tH or resized.shape[1] < tW:
                    break

            # detect edges in the resized, grayscale image and apply template
            # matching to find the template in the image
            result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
            
            """
            # draw a bounding box around the detected region
            clone = np.dstack([edged, edged, edged])
            cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
                    (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
            cv2.imshow("Visualize", clone)
            cv2.waitKey(0)
            """

            # if we have found a new maximum correlation value, then ipdate
            # the bookkeeping variable
            if found is None or maxVal > found[0]:
                    found = (maxVal, maxLoc, r)

    # unpack the bookkeeping varaible and compute the (x, y) coordinates
    # of the bounding box based on the resized ratio
    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

    # draw a bounding box around the detected result and display the image
    cv2.rectangle(img, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(0)


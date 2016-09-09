import cv2, time, imutils
import numpy as np
from matplotlib import pyplot as plt
from skimage import color

def detect_mse(img):
    """ 
    Determines whether the input image contains a stop sign using an image pyramid, a sliding window and 
    a simple MSE comparison. 
    """
    # Reads the input and template images. 
    img = cv2.imread(img)
    tmpl = cv2.imread("img/templates/ss_cheat.jpg")

    (tmpl_height, tmpl_width) = tmpl.shape[:2]
    

    result = cv2.matchTemplate(img, tmpl, cv2.TM_CCOEFF)
    (_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)

    # grab the bounding box of waldo and extract him from
    # the puzzle image
    topLeft = maxLoc
    botRight = (topLeft[0] + tmpl_width, topLeft[1] + tmpl_height)
    roi = img[topLeft[1]:botRight[1], topLeft[0]:botRight[0]]

    # construct a darkened transparent 'layer' to darken everything
    # in the puzzle except for waldo
    mask = np.zeros(img.shape, dtype = "uint8")
    img = cv2.addWeighted(img, 0.25, mask, 0.75, 0)

    # put the original waldo back in the image so that he is
    # 'brighter' than the rest of the image
    img[topLeft[1]:botRight[1], topLeft[0]:botRight[0]] = roi

    # display the images
    cv2.imshow("Puzzle", imutils.resize(img, height = 650))
    cv2.imshow("Waldo", tmpl)
    cv2.waitKey(0)

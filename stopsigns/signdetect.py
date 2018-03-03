import time

import cv2
import imutils
import numpy as np
from skimage.transform import pyramid_gaussian


def detect_haar(classifier, img, example=False):
    """
    Determines whether the input image contains a stop sign using the trained Haar classifier.
    If <example> is set, also draws a rectangle around the detected sign and displays the image.
    """
    # Load the classifier and read the image. 
    classifier = cv2.CascadeClassifier(classifier)
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect any stop signs in the image using the classifier at various scales.
    stop_signs = classifier.detectMultiScale(gray, 1.02, 10)

    if example:
        # Draw a rectangle around each detected sign and display it. 
        for (x,y,w,h) in stop_signs:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
         
        cv2.imshow("img",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # True if any signs were detected. 
        return stop_signs

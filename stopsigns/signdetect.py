import cv2, time, imutils
import numpy as np
from skimage.transform import pyramid_gaussian

def detect_haar(img, example=False):
    """
    Determines whether the input image contains a stop sign using the trained Haar classifier.
    Draws a rectangle around the detected sign if the second parameter is set to True. 
    """

    # Loads the classifier and reads the image. 
    classifier = cv2.CascadeClassifier("stopsign_classifier.xml")
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detects any stop signs in the image using the classifier, resizing at each iteration. 
    stop_signs = classifier.detectMultiScale(gray, 1.02, 10)

    if example == True:
        # Draws a rectangle around each detected sign and displays it. 
        for (x,y,w,h) in stop_signs:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
         
        cv2.imshow('img',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return stop_signs
    else:
        # Returns true if any signs were detected. 
        return stop_signs

def detect_mse(img):
    """ 
    Determines whether the input image contains a stop sign using an image pyramid, a sliding window and 
    a simple MSE comparison. 
    NB: Deprecated. Ineffective, particularly in the case of low-resolution Street View images. 
    """
    # Sets the threshold of acceptance.
    threshold = 0.1

    # Reads the input and template images. 
    img = cv2.imread(img)
    tmpl = cv2.imread("img/templates/stop_sign.jpg")
    
    # Records the best score. 
    best_score = 100000000
    
    # Constructs an image pyramid from the template, halving at each layer and using Gaussian smoothing.
    # http://www.pyimagesearch.com/2015/03/16/image-pyramids-with-python-and-opencv/
    for (i, resized) in enumerate(pyramid_gaussian(tmpl, downscale=1.5)):
        # Breaks if the image is too small. 
        if resized.shape[0] < 16 or resized.shape[1] < 16:
            break

        # Defines sliding window width and height (equal to that of the resized template).
        win_w, win_h = resized.shape[:2]

        # Loops the sliding window over the image.
        for (x, y, window) in sliding_window(img, stepSize=8, windowSize=(win_w, win_h)):
            # Skips window if it is too small. 
            if window.shape[0] != win_h or window.shape[1] != win_w:
                continue

            clone = img.copy()
            cv2.rectangle(clone, (x, y), (x + win_w, y + win_h), (0, 255, 0), 2)
            
            # Computes the MSE of the current window and the template image. 
            score = mse(window, resized)

            # Records the best MSE. 
            if score < best_score:
                best_score = score
                best_match_image = clone

    return best_score < threshold
    
def sliding_window(image, stepSize, windowSize):
    """
    Generates a sliding rectangular window across the input image. 
    http://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/
    """
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # Yields a tuple containing the x and y coordinates of the window and the window itself. 
            yield (x, y, image[y:y+windowSize[1], x:x+windowSize[1]])

def mse(img1, img2):
    """
    Returns the mean-squared error between two images; a smaller MSE indicates more similarity.
    NB: the two images must have the same dimension. 
    http://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
    """
    # Converts the images to floats, takes the difference and squares it.
    err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    
    # Divides by the total number of pixels to yield the mean. 
    err /= float(img1.shape[0] * img2.shape[1])

    return err

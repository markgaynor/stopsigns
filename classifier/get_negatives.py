import os 
import random
import time 
import urllib.request

from config import *

STARTING_LAT = 53.3321281
STARTING_LON = -6.293
STARTING_H = 230
NUM_IMAGES = 1000

if __name__=="__main__":
    """
    Pulls arbitrary images from Streetview in order to build a negative training dataset for the classifier
    in the directory negatives/.
    """
    os.makedirs("negatives", exist_ok=True)

    # Set the desired number of images and the starting coordinates. 
    lt, lg, h = STARTING_LAT, STARTING_LON, STARTING_H

    # Read the template for the image returned by Streetview if a request is invalid. 
    invalid = open("invalid.jpg", "rb").read()

    for i in range(0, NUM_IMAGES + 1):
        # Set the URL according to the current coordinates and grab the image. 
        img_path = "negatives/{}.jpg".format(i)
        url = "https://maps.googleapis.com/maps/api/streetview?size=800x400\
                &location={},&fov=90&heading={}&pitch=10&key={}".format(lt, lg, h, api_key)
        urllib.request.urlretrieve(url, img_path)
        
        # Read the retrieved image and check if it's invalid.
        img = open(img_path, "rb").read()
        if img == invalid:
            # Delete the image, decrement the counter and reset latitude.
            os.remove(path)
            i -= 1
            lt = start
        
        # Increment latitude by a random number between 0 and 0.1. 
        lt += 0.1 * random.random()
        
        # Wait so that we don't make too many API calls.
        time.sleep(0.1)

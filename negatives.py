"""
Pulls arbitrary images from Streetview in order to build a negative training dataset for the classifier. 
"""
import urllib.request, time, os, random, config

# Sets the desired number of images and the starting coordinates. 
no_of_images = 1000
lt, lg, h = 53.29, -6.3, 230

# Reads the image returned by Streetview if a request is invalid. 
invalid = open("invalid.jpg","rb").read()

for i in range(0, no_of_images + 1):
    # Sets the path of the current image. 
    path = "img/negatives/" + str(i) + ".jpg"
    
    # Sets the URL according to the current coordinates and gets the image. 
    url = "https://maps.googleapis.com/maps/api/streetview?size=800x400&location="\
            + str(lt) + "," + str(lg) + "&fov=90&heading=" + str(h) + \
            "&pitch=10&key=" + api_key
    urllib.request.urlretrieve(url, path)
    
    # Reads the image and compares it to the invalid request image. 
    img = open(path, "rb").read()
    if img == invalid:
        # Deletes the image, decrements the counter and resets latitude if the request was invalid. 
        os.remove(path)
        i -= 1
        lt = 53.29
    
    # Increments latitude by a random number between 0 and 0.1. 
    lt += 0.1 * random.random()
    
    # Waits so as not to make too many API calls. 
    time.sleep(0.1)

import json
import logging
import urllib.request

from config import *


def get_img_at_coordinates(lt, lg, h):
    """
    Retrieves a Street View image for a given latitude, longitude and heading, saves it to disk
    and returns the path.
    """
    
    url = "https://maps.googleapis.com/maps/api/streetview?size=800x400&location="\
            + str(lt) + "," + str(lg) + "&fov=90&heading=" + str(h) + \
            "&pitch=10&key=" + api_key

    path = "img/streetviews/lt{}lg{}h{}.jpg".format(lat, lng, h)
    urllib.request.urlretrieve(url, path)

    return path


def resolve_street(address_raw):
    """
    Takes a street name, gets the corresponding coordinates and a retrives Street View images of that point covering every angle.
    Returns a list containing the path of every image retrieved. 
    """
    # Form the url for the Geocoding API call. 
    address = address_raw.replace(" ", "+")
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, api_key)
    
    try:
        # Get the JSON response from the Geocoding API. 
        response = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
        lat = response["results"][0]["geometry"]["location"]["lat"]
        lng = response["results"][0]["geometry"]["location"]["lng"]
    except:
        logger.info("Invalid request. Try again. Only the street name and area are needed.")
        return None
    
    # Retrieve the four StreetView images for that point.
    angles = [0, 90, 180, 270]
    paths = []
    for h in angles:
        path = get_img_at_coordinates(lat, lng, h)
        paths.append(path)
    
    return paths



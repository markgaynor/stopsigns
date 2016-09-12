import urllib.request, json
from config import *

def resolve_street(address_raw):
    """
    Takes a street name, gets the corresponding coordinates and a retrives Street View images of that point covering every angle.
    Returns a list containing the path of every image retrieved. 
    """
    
    # Forms the url for the Geocoding API call. 
    address = address_raw.replace(" ","+")
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=" + api_key
    
    try:
        # Gets the JSON response from the Geocoding API. 
        response = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
        lat = response["results"][0]["geometry"]["location"]["lat"]
        lng = response["results"][0]["geometry"]["location"]["lng"]
    except:
        print("Invalid request. Try again. Only the street name and area are needed.")
        return None
    
    # List to record image file paths.
    paths = []

    # Retrieves the four streetview images for that point.
    angles = [0, 90, 180, 270]
    for h in angles:
        get(lat, lng, h)
        paths.append("img/streetviews/lt" + str(lat) + "lg" + str(lng) + "h" + str(h) + ".jpg")
    
    # Returns the list of paths retrieved. 
    return paths

def get(lt, lg, h):
    """
    Retrieves a Street View image for a given latitude, longitude and heading and saves it to disk.
    """
    
    url = "https://maps.googleapis.com/maps/api/streetview?size=800x400&location="\
            + str(lt) + "," + str(lg) + "&fov=90&heading=" + str(h) + \
            "&pitch=10&key=" + api_key

    path = "img/streetviews/lt" + str(lt) + "lg" + str(lg) + "h" + str(h) + ".jpg"
    urllib.request.urlretrieve(url, path)

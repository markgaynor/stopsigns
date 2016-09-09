import urllib.request, config

def get(lt, lg, h):
    """
    Retrieves a Street View image for a given latitude, longitude and heading and saves it to disk.
    """
    
    url = "https://maps.googleapis.com/maps/api/streetview?size=800x400&location="\
            + str(lt) + "," + str(lg) + "&fov=90&heading=" + str(h) + \
            "&pitch=10&key=" + api_key

    path = "img/streetviews/lt" + str(lt) + "lg" + str(lg) + "h" + str(h) + ".jpg"
    urllib.request.urlretrieve(url, path)

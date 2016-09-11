from stopsigns import streetviews
from stopsigns import signdetect

lt, lg, h = 53.2905066, -6.2865601, 230
streetviews.get(lt, lg, h)

img = "img/streetviews/lt" + str(lt) + "lg" + str(lg) + "h" + str(h) + ".jpg"

signdetect.detect_haar(img)

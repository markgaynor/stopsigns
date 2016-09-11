from stopsigns import streetviews
from stopsigns import signdetect

# Gets an area from the user. 
address = "20 Stonepark Abbey, Rathfarnham, Dublin"
coords = None
streetviews.resolve_street(address)


#lt, lg, h = 53.2905066, -6.2865601, 230
#streetviews.get(lt, lg, h)
#img = "img/streetviews/lt" + str(lt) + "lg" + str(lg) + "h" + str(h) + ".jpg"
#signdetect.detect_haar(img)


from stopsigns import streetviews
from stopsigns import signdetect

if __name__=="__main__":
    lt, lg, h = 53.2905066, -6.2865601, 230
    path = streetviews.get_img_at_coordinates(lt, lg, h)

    signdetect.detect_haar(path, True)

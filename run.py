from stopsigns import streetviews
from stopsigns import signdetect
import sys, os

print("*** STOP SIGN DETECTOR ***\n")
        
# Gets an area from the user, resolves it to coordinates and gets a Street View image covering every angle.
address = input("Provide an address: ")
images = streetviews.resolve_street(address)

# Checks each of those images for a stop sign.
for image in images:
    if len(signdetect.detect_haar(image)) > 0:
        print("Stop sign detected.")
        sys.exit()

print("No stop sign detected.")

# Cleans up.
for image in images:
    os.remove(image)


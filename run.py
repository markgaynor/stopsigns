import sys
import os
import logging
logging.basicConfig(level=logging.DEBUG, format="%(message)s")

from stopsigns import streetviews
from stopsigns import signdetect

def clean_up(images):
    # Clean up.
    for image in images:
        os.remove(image)


if __name__=="__main__":
    logging.info("*** STOP SIGN DETECTOR ***\n")
        
    # Get an area from the user, resolve it to coordinates and get Street View images covering every angle.
    address = input("Provide an address: ")
    images = streetviews.resolve_street(address)

    # Check each of those images for a stop sign.
    for image in images:
        if len(signdetect.detect_haar(image, "classifier.xml")) > 0:
            logging.info("Stop sign detected. Exiting...")
            clean_up(images)
            sys.exit(1)

    logging.info("No stop sign detected.")
    clean_up(images)


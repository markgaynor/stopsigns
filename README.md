# Stop sign detection in Google Street View with Python and OpenCV

Detects stop signs in Google Street View images of a provided address using a Haar cascade classifier.

Also provides functionality to detect stop signs using feature matching, though this was deprecated due to inaccuracy (particularly over low-resolution Street View images). 

![Example of stop sign detection](https://raw.githubusercontent.com/markgaynor/stopsigns/master/example.png)

### Requirements
Python 3.x
OpenCV 3

NB: Depending on your Python environment, OpenCV may have to be manually compiled. 
For Anaconda: ```conda install -c https://conda.binstar.org/menpo opencv3```

Python modules:
pip install -r requirements.txt 

### Usage
Maps API key should be assigned to the variable ```api_key``` in /config.py

Run ```example.py``` for an example of stop sign detection.
Run ```run.py``` and provide an address to detect whether there is a stop sign at that address.

### Attribution
Classifier training was done following examples from Naotoshi Seo and Thorsten Ball.
The (deprecated) template matching method followed examples from pyimagesearch.com.

http://note.sonots.com/SciSoftware/haartraining.html
http://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html
http://www.pyimagesearch.com/

All map and Street View content © Google. 

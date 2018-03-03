# Stop sign detection in Google Street View with Python and OpenCV

Takes an address, and determines whether or not there is a stop sign there using Google Street View and a simple 24x24 Haar cascade classifier.

![Example of stop sign detection](https://raw.githubusercontent.com/markgaynor/stopsigns/master/example.png)

### Requirements
* Python 3.x
* OpenCV 3

NB: Depending on your environment, `OpenCV` may have to be built from source. 

(Easy installation using Anaconda (x86): `conda install -c https://conda.binstar.org/menpo opencv3`)

* Python modules: `pip install -r requirements.txt`

### Usage
Maps API key should be assigned to the variable `api_key` in `config.py`. 

Run `example.py` for an example of stop sign detection.

Run `run.py` and provide an address in order to detect stop signs at that address.

### Attribution
Classifier training was done following examples from Naotoshi Seo and Thorsten Ball.

* http://note.sonots.com/SciSoftware/haartraining.html/
* http://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html/

All map and Street View content © Google. 

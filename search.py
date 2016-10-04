# author: Adrian Rosebrock
# date: 27 January 2014
# website: http://www.pyimagesearch.com

# USAGE
# python search.py --dataset images --index index.cpickle

# import the necessary packages
from pyimagesearch.searcher import Searcher
import numpy as np
import argparse
import cPickle
import cv2

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-d", "--dataset", required = True,
#	help = "Path to the directory that contains the images we just indexed")
# ap.add_argument("-i", "--index", required = True,
#	help = "Path to where we stored our index")
# args = vars(ap.parse_args())

# load the index and initialize our searcher
index = cPickle.loads(open("index").read())
searcher = Searcher(index)

# Directory
directory = "images"  # "faces/s1"

# loop over images in the index -- we will use each one as
# a query image
for (query, queryFeatures) in index.items():
    # perform the search using the current query
    results = searcher.search(queryFeatures)
    # load the query image and display it
    path = directory + "/%s" % (query)
    queryImage = cv2.imread(path)
    cv2.imshow("Query", queryImage)
    print "query: %s" % (query)

    # initialize the two montages to display our results --
    # we have a total of 25 images in the index, but let's only
    # display the top 10 results; 5 images per montage, with
    # images that are 400x166 pixels
    # montageA = np.zeros((92 * 5, 112, 3), dtype="uint8")
    # montageB = np.zeros((92 * 5, 112, 3), dtype="uint8")
    montageA = np.zeros((166 * 5, 400, 3), dtype="uint8")
    montageB = np.zeros((166 * 5, 400, 3), dtype="uint8")

    # loop over the top ten results
    for j in xrange(0, 10):
        # grab the result (we are using row-major order) and
        # load the result image
        print "J: ", j
        (score, imageName) = results[j]
        path = directory + "/%s" % (imageName)
        result = cv2.imread(path)
        print "Result: ", result
        print "\t%d. %s : %.3f" % (j + 1, imageName, score)

        # check to see if the first montage should be used
        if j < 5:
            montageA[j * 166:(j + 1) * 166, :] = result

        # otherwise, the second montage should be used
        else:
            montageB[(j - 5) * 166:((j - 5) + 1) * 166, :] = result

    # show the results
    cv2.imshow("Results 1-5", montageA)
    cv2.imshow("Results 6-10", montageB)
    cv2.waitKey(0)

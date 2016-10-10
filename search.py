from pyimagesearch.searcher import Searcher
import PIL
from PIL import Image
import numpy as np
import cPickle
import cv2
import subprocess

index = cPickle.loads(open("index").read())
searcher = Searcher(index)

directory = "mammogram"

for (query, queryFeatures) in index.items():
    # perform the search using the current query
    results = searcher.search(queryFeatures)
    # load the query image and display it
    path = directory + "/%s" % (query)
    image = cv2.imread(path)
    newx, newy = image.shape[1] / 6, image.shape[0] / 6
    newimage = cv2.resize(image, (newx, newy))
    cv2.imshow("Query", newimage)
    print "query: %s" % (query)

    montageA = np.zeros((170 * 50, 170, 3), dtype="uint8")
    for j in xrange(0, 50):
        (score, imageName) = results[j]
        path = directory + "/%s" % (imageName)
        image = cv2.imread(path)
        newx, newy = image.shape[1] / 6, image.shape[0] / 6
        newimage = cv2.resize(image, (newx, newy))
        cv2.imshow(imageName, newimage)
        print "\t%d. %s : %.3f" % (j + 1, imageName, score)
    cv2.waitKey(0)

    # show the results
    #cv2.imshow("Show results", montageA)
    #cv2.waitKey(0)
    #print "size", len(montageA)
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

    listImage1 = np.zeros((170 * 5, 170, 3), dtype="uint8")
    listImage2 = np.zeros((170 * 5, 170, 3), dtype="uint8")
    for j in xrange(0, 10):
        (score, imageName) = results[j]
        path = directory + "/%s" % (imageName)
        image = cv2.imread(path)
        newx, newy = image.shape[1] / 6, image.shape[0] / 6
        newimage = cv2.resize(image, (newx, newy))
        #cv2.imshow(imageName, newimage)
        print "\t%d. %s : %.3f" % (j + 1, imageName, score)
        # check to see if the first montage should be used
        if j < 5:
            listImage1[j * 170:(j + 1) * 170, :] = newimage

        # otherwise, the second montage should be used
        else:
            listImage2[(j - 5) * 170:((j - 5) + 1) * 170, :] = newimage

    # show the results
    cv2.imshow("Results 1-5", listImage1)
    cv2.imshow("Results 6-10", listImage2)
    cv2.waitKey(0)
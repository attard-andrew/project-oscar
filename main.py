#! python3
# main.py - Primary script for project Oscar, a tool for identifying and grouping
# 			    similar images locally

from PIL import Image
import imagehash
import argparse
import shelve
import glob
import pprint

# Create the argument parser object
ap = argparse.ArgumentParser(description='Parse source directory and shelf arguments')
ap.add_argument("-d", "--dataset", required = True,
    help = "path to input dataset of images")
ap.add_argument("-s", "--shelve", required = True,
    help = "output shelve database")

# parse the agruments
args = vars(ap.parse_args())

# open the shelve database
db = shelve.open(args["shelve"], writeback = True)

# loop over the image dataset
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):

    # C:/images/*.jpg
    # load the image and compute the difference hash
    image = Image.open(imagePath)
    h = str(imagehash.dhash(image))

    # extract the filename from the path and update the database
    # using the hash as the key and the filename append to the 
    # list of values

    filename = imagePath[imagePath.rfind("/") + 1:]
    db[h] = db.get(h, []) + [filename]

# display shelve data
for item in db.keys():
    print(item + ': ' + str(db[item]))

# close the shelf database
db.close

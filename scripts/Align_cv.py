from __future__ import print_function
import cv2
import numpy as np

class Align_cv:


    def __init__(self):
        self.MAX_FEATURES = 200
        self.GOOD_MATCH_PERCENT = 0.15 


    def alignImages(self,im1, im2):

        print("Alignement...")
        # Convert images to grayscale
        im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        # Detect ORB features and compute descriptors.
        orb = cv2.ORB_create(self.MAX_FEATURES)
        #sift = cv2.SIFT_create(self.MAX_FEATURES)
        keypoints1 = orb.detect(im1Gray, None)
        keypoints1, descriptors1 = orb.compute(im1Gray, keypoints1)
        keypoints2 = orb.detect(im2Gray, None)
        keypoints2, descriptors2 = orb.compute(im2Gray, keypoints2)
        # Match features.
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        #matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(descriptors1, descriptors2, None)
        # Sort matches by score
        matches = sorted(matches, key=lambda x: x.distance, reverse=False)
        # Remove not so good matches
        numGoodMatches = int(len(matches) * self.GOOD_MATCH_PERCENT)
        matches = matches[:numGoodMatches]
        # Draw top matches
        imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
        cv2.imwrite("matches.jpg", imMatches)

        # Extract location of good matches
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt
            points2[i, :] = keypoints2[match.trainIdx].pt

        # Find homography
        h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

        # Use homography
        height, width, channels = im2.shape
        im1Reg = cv2.warpPerspective(im1, h, (width, height))

        return im1Reg, h

    def loadRef(self, refFilename):

        print("Reading reference image : ", refFilename)
        imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

        return imReference

    def loadIm(self, imFilename):

        print("Reading image to align : ", imFilename)
        im = cv2.imread(imFilename, cv2.IMREAD_COLOR)

        return im

    def saveIm(self, im, outFilename):

        print("Saving aligned image : ", outFilename)
        cv2.imwrite(outFilename, im)




    

if __name__ == '__main__':

    a = Align_cv()
    # Read reference image
    refFilename = '../input/DSC_9387-Panorama.jpg'
    
    imReference = a.loadRef(refFilename)

    # Read image to be aligned
    imFilename = '../input/DSC_9439-Panorama.jpg'
    im = a.loadIm(imFilename)

    print("Aligning images ...")
    # Registered image will be resotred in imReg.
    # The estimated homography will be stored in h.

    imReg, h = a.alignImages(im, imReference)
    # Write aligned image to disk.
    outFilename = "aligned.jpg"
    a.saveIm(imReg, outFilename)

    # Print estimated homography
    print("Estimated homography : \n",  h)

# -*- coding: utf-8 -*-

import sys
import os.path

import cv2
import cv2.cv as cv

def normalize(filename, indir, outdir):
    filepath = os.path.join(indir, filename)
    img = cv2.imread(filepath)
    cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces_rect = cascade.detectMultiScale(img, minNeighbors=4, minSize=(30, 30),
                                          flags=cv.CV_HAAR_SCALE_IMAGE)
    if len(faces_rect) != 1:
        return
    
    faces_rect[:,2:] += faces_rect[:,:2]
    x1, y1, x2, y2 = faces_rect[0]

    outpath = os.path.join(outdir, filename)
    cv2.imwrite(outpath, img[y1:y2, x1:x2])
    

def proc(indir, outdir):
    for dirname, dirnames, filenames in os.walk(indir):
        for filename in filenames:
            normalize(filename, indir, outdir)
            
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: python normalize.py [indir] [outdir]')
    proc(sys.argv[1], sys.argv[2])

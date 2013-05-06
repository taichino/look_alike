# -*- coding: utf-8 -*-

import sys
import os.path
from django.conf import settings

import cv2
import numpy as np
from scipy.spatial import distance

from sklearn.decomposition import PCA


def img2mat(img):
    shape = img.shape
    img = np.asanyarray(img, dtype=np.float32)
    img = img.flatten() / 255.0
    return img

def read_images(path, sz=None):
    print path
    c = 0
    X, y = [], []
    filenames = []
    for filename in os.listdir(path):
        try:
            if 'jpg' not in filename: continue
            im = cv2.imread(os.path.join(path, filename), cv2.IMREAD_GRAYSCALE)
            if (sz is not None):
                im = cv2.resize(im, sz)
            X.append(img2mat(im))
            y.append(c)
            filenames.append(filename)
        except IOError, (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        c += 1
    return [X, y, filenames]


model = None
def get_recognition_model():
    global model
    if model: return model
    
    dir_path = os.path.join(settings.MEDIA_ROOT, 'normalized')
    X, y, filenames = read_images(dir_path, (64, 64))
    pca = PCA(n_components=0.8)
    pca.fit(X, y)
    features = pca.transform(X)
    labels = np.asarray(y)

    model = (pca, features, labels, filenames)
    return model

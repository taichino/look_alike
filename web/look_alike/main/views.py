# -*- coding: utf-8 -*-

import sys
import os
import os.path
import urllib
import json
import tempfile

import cv2
import numpy as np
from scipy.spatial import distance

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

from main.recognizer import get_recognition_model, img2mat

@csrf_exempt
def top(request):
    print 'top'
    image_data = None
    for filename, file in request.FILES.iteritems():
        image_data = request.FILES[filename].read()

    if image_data:
        f = open('/tmp/face.png', 'wb+')
        f.write(image_data)
        f.close()
    
        (pca, features, labels, filenames) = get_recognition_model()

        # path = os.path.join(settings.MEDIA_ROOT, 'normalized', 'A.J Langer.jpg')
        # im = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (64, 64))
        im = cv2.resize(cv2.imread('/tmp/face.png', cv2.IMREAD_GRAYSCALE), (64, 64))
        im = img2mat(im)
        feature_coef = np.array(pca.components_.T, np.float64)
        query_feature = np.dot(im, feature_coef)
        distances = distance.cdist(features, [query_feature]).flatten()
        closest_idx = distances.argmin()
        name = filenames[closest_idx]
    
        url = '/media/orig/%s' % (name)
        data = {'name':name.replace('.jpg', ''), 'url':urllib.quote(url)}
    
        return HttpResponse(json.dumps(data), mimetype="application/json")

    return HttpResponse(json.dumps({'msg':'no image data'}))
        

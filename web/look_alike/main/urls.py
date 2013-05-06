# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'main.views',

    url(r'^$', 'top', name='top'),
)

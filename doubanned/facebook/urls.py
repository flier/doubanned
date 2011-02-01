#!/usr/bin/env python

__author__ = 'Flier Lu'

from django.conf.urls.defaults import *

urlpatterns = patterns('doubanned.facebook.views',
    (r'^$', 'index'),
)

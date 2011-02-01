#!/usr/bin/env python

__author__ = 'Flier Lu'

from django.conf.urls.defaults import *

urlpatterns = patterns('doubanned.douban.views',
    (r'^$', 'index'),
)

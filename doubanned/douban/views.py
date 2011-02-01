#!/usr/bin/env python
from django.http import HttpResponse

try:
    import simplejson as json
except ImportError:
    import json

import gdata.alt.appengine

import douban.service

from key import *

def index(request):

    svc = douban.service.DoubanService(api_key=DOUBAN_APP_KEY, secret=DOUBAN_APP_SECRET)

    gdata.alt.appengine.run_on_appengine(svc)

    return HttpResponse("It works")
#!/usr/bin/env python
from django.http import HttpResponse

try:
    import simplejson as json
except ImportError:
    import json

from facebook import *

__author__ = 'Flier Lu'

def default(request):
    return HttpResponse("Bingo, it works!")

def facebook(request):
    data = parse_signed_request(request)

    if not data.has_key('user_id'):
        request_url = oauth_request_url()
        
        return HttpResponse("<script>top.location.href='%s';</script>" % request_url)

    return HttpResponse("Welcome %s" % data['user_id'])
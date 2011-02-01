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


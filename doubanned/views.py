#!/usr/bin/env python
from django.http import HttpResponse

__author__ = 'Flier Lu'

def default(request):
    return HttpResponse("Bingo, it works!")
  
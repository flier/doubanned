#!/usr/bin/env python
import hashlib

from django import template
from django.core.urlresolvers import reverse

from doubanned.settings import *

__author__ = 'Flier Lu'

register = template.Library()

def static_url(path):
    return "%s%s" % (STATIC_DOC_PREFIX, path)

def reverse_url(name):
    return reverse(name)

def md5(text):
    return hashlib.md5(text).hexdigest()

def icon(name):
    return '<img src="%s" alt="%s" class="icon"/>' % (static_url("icon/%s.ico" % name), name)

register.filter(static_url)
register.filter(reverse_url)
register.filter(md5)
register.filter(icon)
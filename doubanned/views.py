#!/usr/bin/env python
import logging
from google.appengine.api import users

from django.shortcuts import render_to_response
    
__author__ = 'Flier Lu'

def default(request):
    user = users.get_current_user()

    return render_to_response('index.html', {
        'user': user,
        'login_url': users.create_login_url('/'),
        'logout_url': users.create_logout_url('/'),
    })


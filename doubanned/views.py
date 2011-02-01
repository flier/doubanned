#!/usr/bin/env python
from google.appengine.api import users

from django.shortcuts import render_to_response

from doubanned.douban.models import DoubanUser
from doubanned.settings import *
    
__author__ = 'Flier Lu'

def default(request):
    user = users.get_current_user()

    douban_users = DoubanUser.find(user) if user else None

    return render_to_response('index.html', {
        'debug': DEBUG,
        'user': user,
        'douban_users': douban_users,
        'login_url': users.create_login_url('/'),
        'logout_url': users.create_logout_url('/'),
    })


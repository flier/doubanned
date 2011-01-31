#!/usr/bin/env python
from urllib import urlencode
from base64 import urlsafe_b64decode

try:
    import simplejson as json
except ImportError:
    import json

import hmac
from hashlib import sha256

from facebook_key import *

FACEBOOK_APP_NAME = 'doubanned'
FACEBOOK_APP_CANVAS_PAGE = 'http://apps.facebook.com/doubanned/'
FACEBOOK_APP_CANVAS_URL = 'http://doubanned.appspot.com/facebook/'

def base64_url_decode(encoded):
    return urlsafe_b64decode(encoded + ('=' * (4 - (len(encoded) % 4))))

def parse_signed_request(request):
    encoded_sig, payload = request.REQUEST['signed_request'].split('.')

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data['algorithm'].upper() != 'HMAC-SHA256':
        raise NotImplementedError("Unknown algorithm: %s" % data['algorithm'])

    if request.META['SERVER_NAME'] != 'localhost':
        expected_sig = hmac.new(FACEBOOK_APP_SECRET, payload, sha256).digest()

        if expected_sig != sig:
            raise Exception("Bad Signed JSON signature")

    return data

def oauth_request_url():
    params = {
        'client_id': FACEBOOK_APP_ID,
        'redirect_uri': FACEBOOK_APP_CANVAS_PAGE,
    }
    
    return "https://www.facebook.com/dialog/oauth?" + urlencode(params)
#!/usr/bin/env python
import sys, new
import logging

from django.http import HttpResponse
from django.utils.translation import gettext, ngettext
from django.core.exceptions import ImproperlyConfigured

__author__ = 'Flier Lu'

def is_ajax(self):
    return self.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def get_header(self, name, default):
    return self.headers.get(name, default)

class HttpResponseBadRequest(HttpResponse):
    status_code = 400

def url(regex, view, name=None):
    return (regex, view,)

def force_unicode(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_unicode, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, basestring,):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                try:
                    s = unicode(str(s), encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(s, Exception):
                        raise
                    # If we get to here, the caller has passed in an Exception
                    # subclass populated with non-ASCII data without special
                    # handling to display as a string. We need to handle this
                    # without raising a further exception. We do an
                    # approximation to what the Exception's standard str()
                    # output should be.
                    s = ' '.join([force_unicode(arg, encoding, strings_only,
                            errors) for arg in s])
        elif not isinstance(s, unicode):
            # Note: We use .decode() here, instead of unicode(s, encoding,
            # errors), so that if s is a SafeString, it ends up being a
            # SafeUnicode at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError, e:
        if not isinstance(s, Exception):
            raise DjangoUnicodeDecodeError(s, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = ' '.join([force_unicode(arg, encoding, strings_only,
                    errors) for arg in s])
    return s

def ugettext(message):
    return force_unicode(gettext(message))

def ungettext(singular, plural, number):
    return force_unicode(ngettext(singular, plural, number))

def complain(*args, **kwargs):
    raise ImproperlyConfigured, "You haven't set the DATABASE_ENGINE setting yet."

class DatabaseError(Exception):
    pass

class DatabaseWrapper:
    def __init__(self, **kwargs):
        pass

    def close(self):
        pass # close()

    cursor = complain
    _commit = complain
    _rollback = complain

import django.dispatch

class Signal(object):
    def __init__(self, providing_args=None):
        self.providing_args = providing_args

    def connect(self, receiver, sender=None, weak=True, dispatch_uid=None):
        django.dispatch.connect(receiver, self, sender, weak)

def safe(value):
    """
    Marks the value as a string that should not be auto-escaped.
    """
    return value

def in_appengine():
    try:
        import google.appengine

        return True
    except ImportError:
        return False

def setup_hotfix():
    logging.info("patching django debug toolbar for appengine ...")

    sys.modules['django.db.backends.appengine'] = new.module('django.db.backends.appengine')
    sys.modules['django.db.backends'] = new.module('django.db.backends')

    backend = new.module('django.db.backends.appengine.base')
    backend.DatabaseWrapper = DatabaseWrapper
    backend.DatabaseError = DatabaseError

    backend.supports_constraints = False
    backend.quote_name = complain
    backend.dictfetchone = complain
    backend.dictfetchmany = complain
    backend.dictfetchall = complain
    backend.get_last_insert_id = complain
    backend.get_date_extract_sql = complain
    backend.get_date_trunc_sql = complain
    backend.get_limit_offset_sql = complain
    backend.get_random_function_sql = complain
    backend.get_deferrable_sql = complain
    backend.get_fulltext_search_sql = complain
    backend.get_drop_foreignkey_sql = complain
    backend.get_sql_flush = complain
    backend.OPERATOR_MAPPING = {}
    sys.modules['django.db.backends.appengine.base'] = backend

    import django.http
    django.http.HttpRequest.is_ajax = is_ajax
    django.http.HttpResponse.get = get_header
    django.http.HttpResponseBadRequest = HttpResponseBadRequest

    import django.conf.urls.defaults
    django.conf.urls.defaults.url = url
    django.conf.urls.defaults.__all__.append('url')

    import django.utils
    import hashlib
    hashcompat = new.module('django.utils.hashcompat')
    hashcompat.md5_hmac = hashcompat.md5_constructor = hashlib.md5
    hashcompat.sha_hmac = hashcompat.sha_constructor = hashlib.sha1
    sys.modules['django.utils.hashcompat'] = hashcompat

    from django.newforms.util import smart_unicode

    encoding = new.module('django.utils.encoding')
    encoding.__all__ = ['smart_unicode', 'force_unicode']
    encoding.smart_unicode = smart_unicode
    encoding.force_unicode = force_unicode
    sys.modules['django.utils.encoding'] = django.utils.encoding = encoding

    from django.utils.functional import lazy
    import django.utils.translation
    django.utils.translation.ugettext_lazy = lazy(ugettext, unicode)
    django.utils.translation.ungettext_lazy = lazy(ungettext, unicode)

    import django.dispatch
    django.dispatch.Signal = Signal

    import django.test.signals
    django.test.signals.template_rendered = Signal(providing_args=["template", "context"])

    from django.template.defaultfilters import register

    register.filter(safe)
    
if in_appengine():
    try:
        setup_hotfix()
    except:
        import traceback

        traceback.print_exc()

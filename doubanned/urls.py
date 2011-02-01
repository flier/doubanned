from django.conf.urls.defaults import *

from doubanned.settings import *

urlpatterns = patterns('',
    (r'douban/', include('doubanned.douban.urls')),
    (r'facebook/', include('doubanned.facebook.urls')),

    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': STATIC_DOC_ROOT }),
    (r'^$', 'doubanned.views.default'),
)

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'douban/', include('doubanned.douban.urls')),
    (r'facebook/', include('doubanned.facebook.urls')),
    (r'', 'doubanned.views.default'),
)

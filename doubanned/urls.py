from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'facebook/', include('doubanned.facebook.urls')),
    (r'', 'doubanned.views.default'),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)

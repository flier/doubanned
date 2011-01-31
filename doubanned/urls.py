from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^doubanned/', include('doubanned.foo.urls')),
    (r'', 'doubanned.views.default')

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)


from django.conf.urls import *

urlpatterns = patterns('leonardo_package_index.apps.views',
                       url(r'^api/', include('leonardo_package_index.api.urls'),),
                       )

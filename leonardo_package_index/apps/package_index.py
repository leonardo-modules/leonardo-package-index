
from django.conf.urls import *

urlpatterns = patterns('leonardo_package_index.apps.views',
                       (r'^$', 'package_list', {}, 'package_list'),
                       (r'^packages/(?P<object_slug>[\-\w]+)/$',
                        'package_detail', {}, 'package_detail'),
                       (r'^categories/$', 'category_list', {}, 'category_list'),
                       (r'^categories/(?P<object_slug>[\-\w]+)/$',
                        'category_detail', {}, 'category_detail'),
                       )

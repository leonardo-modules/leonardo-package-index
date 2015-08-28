
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo_package_index.Config'


LEONARDO_APPS = [
    'leonardo_package_index',
]

LEONARDO_OPTGROUP = 'Leonardo Packages'

LEONARDO_WIDGETS = [
    PackageListWidget,
]


LEONARDO_PLUGINS = [
    ('leonardo_package_index.apps.package_index', ('Package List'), ),
]


class Config(AppConfig):
    name = 'leonardo_package_index'
    verbose_name = ("Leonardo Package Index")

from __future__ import absolute_import

import logging

from leonardo_package_index.models import Category, Package
from rest_framework.permissions import AllowAny

from .base import BaseViewSet
from .serializers import *

LOG = logging.getLogger(__name__)


class PackageIndexViewSet(BaseViewSet):
    permission_classes = [AllowAny]


class PackageViewSet(PackageIndexViewSet):

    serializer_class = PackageSerializer
    queryset = Package.objects.all()


class CategoryViewSet(PackageIndexViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import ListWidget
from django.db import models


class PackageListWidget(ListWidget):

    categories = models.ManyToManyField('leonardo_package_index.Category', blank=True)

    def get_items(self, request=None):
        packages = []
        for category in self.categories.all():
            packages += category.package_set.all()
        return packages

    class Meta:
        abstract = True
        verbose_name = _('Package list')
        verbose_name_plural = _('Package lists')

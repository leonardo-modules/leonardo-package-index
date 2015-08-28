# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leonardo_package_index', '0002_auto_20150828_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='pypi_description',
            field=markupfield.fields.MarkupField(default=b'', rendered_field=True, verbose_name='text', blank=True),
        ),
    ]

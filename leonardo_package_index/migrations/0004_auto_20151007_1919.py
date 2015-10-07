# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leonardo_package_index', '0003_auto_20150828_2328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='show_pypi',
        ),
        migrations.AddField(
            model_name='package',
            name='show_pypi',
            field=models.BooleanField(default=True, verbose_name='Show pypi stats & version'),
        ),
        migrations.RemoveField(
            model_name='package',
            name='category',
        ),
        migrations.AddField(
            model_name='package',
            name='category',
            field=models.ManyToManyField(to='leonardo_package_index.Category', verbose_name=b'Installation', blank=True),
        ),
    ]

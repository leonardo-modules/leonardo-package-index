# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leonardo_package_index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='_pypi_description_rendered',
            field=models.TextField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='pypi_description',
            field=markupfield.fields.MarkupField(default='Empty text', rendered_field=True, verbose_name='text', blank=True),
        ),
        migrations.AddField(
            model_name='package',
            name='pypi_description_markup_type',
            field=models.CharField(default=b'restructuredtext', max_length=30, blank=True, choices=[(b'', b'--'), (b'html', 'HTML'), (b'plain', 'Plain'), (b'markdown', 'Markdown'), (b'restructuredtext', 'Restructured Text')]),
        ),
    ]

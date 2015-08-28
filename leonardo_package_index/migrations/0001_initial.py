# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=b'50', verbose_name='Title')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('title_plural', models.CharField(max_length=b'50', verbose_name='Title Plural', blank=True)),
                ('show_pypi', models.BooleanField(default=True, verbose_name='Show pypi stats & version')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('commit_date', models.DateTimeField(verbose_name='Commit Date')),
                ('commit_hash', models.CharField(default=b'', help_text=b'Example: Git sha or SVN commit id', max_length=150, verbose_name='Commit Hash', blank=True)),
            ],
            options={
                'ordering': ['-commit_date'],
                'get_latest_by': 'commit_date',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=b'100', verbose_name='Title')),
                ('slug', models.SlugField(help_text=b"Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens. Values will be converted to lowercase.", unique=True, verbose_name='Slug')),
                ('repo_description', models.TextField(verbose_name='Repo Description', blank=True)),
                ('repo_url', models.URLField(help_text=b'Enter your project repo hosting URL here. Example: https://github.com/opencomparison/opencomparison', unique=True, verbose_name='repo URL', blank=True)),
                ('repo_watchers', models.IntegerField(default=0, verbose_name='Stars')),
                ('repo_forks', models.IntegerField(default=0, verbose_name='repo forks')),
                ('pypi_url', models.CharField(default=b'', help_text=b'<strong>Leave this blank if this package does not have a PyPI release.</strong> What PyPI uses to index your package. Example: django-uni-form', max_length=255, verbose_name='PyPI slug', blank=True)),
                ('pypi_downloads', models.IntegerField(default=0, verbose_name='Pypi downloads')),
                ('participants', models.TextField(help_text=b'List of collaborats/participants on the project', verbose_name='Participants', blank=True)),
                ('last_fetched', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('documentation_url', models.URLField(default=b'', null=True, verbose_name='Documentation URL', blank=True)),
                ('commit_list', models.TextField(verbose_name='Commit List', blank=True)),
                ('category', models.ForeignKey(verbose_name=b'Installation', to='leonardo_package_index.Category')),
                ('created_by', models.ForeignKey(related_name='creator', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('last_modified_by', models.ForeignKey(related_name='modifier', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('usage', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['title'],
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='PackageExample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=b'100', verbose_name='Title')),
                ('url', models.URLField(verbose_name='URL')),
                ('active', models.BooleanField(default=True, help_text=b'Moderators have to approve links before they are provided', verbose_name='Active')),
                ('package', models.ForeignKey(to='leonardo_package_index.Package')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('number', models.CharField(default=b'', max_length=b'100', verbose_name='Version', blank=b'')),
                ('downloads', models.IntegerField(default=0, verbose_name='downloads')),
                ('license', models.CharField(max_length=b'100', verbose_name='license')),
                ('hidden', models.BooleanField(default=False, verbose_name='hidden')),
                ('upload_time', models.DateTimeField(help_text='When this was uploaded to PyPI', null=True, verbose_name='upload_time', blank=True)),
                ('development_status', models.IntegerField(default=0, verbose_name='Development Status', choices=[(0, b'Unknown'), (1, b'Development Status :: 1 - Planning'), (2, b'Development Status :: 2 - Pre-Alpha'), (3, b'Development Status :: 3 - Alpha'), (4, b'Development Status :: 4 - Beta'), (5, b'Development Status :: 5 - Production/Stable'), (6, b'Development Status :: 6 - Mature'), (7, b'Development Status :: 7 - Inactive')])),
                ('supports_python3', models.BooleanField(default=False, verbose_name='Supports Python 3')),
                ('package', models.ForeignKey(blank=True, to='leonardo_package_index.Package', null=True)),
            ],
            options={
                'ordering': ['-upload_time'],
                'get_latest_by': 'upload_time',
            },
        ),
        migrations.AddField(
            model_name='commit',
            name='package',
            field=models.ForeignKey(to='leonardo_package_index.Package'),
        ),
    ]

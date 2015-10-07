import json
import re
from datetime import datetime, timedelta
from django.utils import timezone

import requests
from distutils.version import LooseVersion as versioner
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from leonardo_package_index.repos import get_repo_for_repo_url
from leonardo_package_index.utils import (STATUS_CHOICES, get_pypi_version,
                                          get_version, normalize_license,
                                          status_choices_switch)
from markupfield.fields import MarkupField
from .base import BaseModel

repo_url_help_text = settings.PACKAGINATOR_HELP_TEXT['REPO_URL']
pypi_url_help_text = settings.PACKAGINATOR_HELP_TEXT['PYPI_URL']


class NoPyPiVersionFound(Exception):
    pass


class Category(BaseModel):

    title = models.CharField(_("Title"), max_length="50")
    slug = models.SlugField(_("slug"))
    description = models.TextField(_("description"), blank=True)
    title_plural = models.CharField(_("Title Plural"), max_length="50", blank=True)

    @property
    def count(self):
        return self.package_set.count()

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy('package_index:category_detail',
                                         kwargs={
                                             'object_slug': self.slug
                                         })


class Package(BaseModel):

    title = models.CharField(_("Title"), max_length="100")
    slug = models.SlugField(
        _("Slug"), help_text="Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens. Values will be converted to lowercase.", unique=True)
    category = models.ManyToManyField(Category, verbose_name="Installation", blank=True)
    repo_description = models.TextField(_("Repo Description"), blank=True)
    repo_url = models.URLField(
        _("repo URL"), help_text=repo_url_help_text, blank=True, unique=True)
    repo_watchers = models.IntegerField(_("Stars"), default=0)
    repo_forks = models.IntegerField(_("repo forks"), default=0)
    pypi_url = models.CharField(
        _("PyPI slug"), max_length=255, help_text=pypi_url_help_text, blank=True, default='')
    pypi_downloads = models.IntegerField(_("Pypi downloads"), default=0)
    pypi_description = MarkupField(
        _('text'), blank=True, default='', default_markup_type='restructuredtext')
    participants = models.TextField(_("Participants"),
                                    help_text="List of collaborats/participants on the project", blank=True)
    usage = models.ManyToManyField(User, blank=True)
    created_by = models.ForeignKey(
        User, blank=True, null=True, related_name="creator", on_delete=models.SET_NULL)
    last_modified_by = models.ForeignKey(
        User, blank=True, null=True, related_name="modifier", on_delete=models.SET_NULL)
    last_fetched = models.DateTimeField(blank=True, null=True, default=timezone.now)
    documentation_url = models.URLField(
        _("Documentation URL"), blank=True, null=True, default="")

    commit_list = models.TextField(_("Commit List"), blank=True)
    show_pypi = models.BooleanField(_("Show pypi stats & version"), default=True)

    @property
    def description(self):
        from markupfield.markup import render_rest
        if self.repo_description:
            return render_rest(self.repo_description)
        return self.pypi_description

    @property
    def pypi_name(self):
        """ return the pypi name of a package"""

        if not self.pypi_url.strip():
            return ""

        name = self.pypi_url.replace("http://pypi.python.org/pypi/", "")
        if "/" in name:
            return name[:name.index("/")]
        return name

    def last_updated(self):
        cache_name = self.cache_namer(self.last_updated)
        last_commit = cache.get(cache_name)
        if last_commit is not None:
            return last_commit
        try:
            last_commit = self.commit_set.latest('commit_date').commit_date
            if last_commit:
                cache.set(cache_name, last_commit)
                return last_commit
        except ObjectDoesNotExist:
            last_commit = None

        return last_commit

    @property
    def repo(self):
        return get_repo_for_repo_url(self.repo_url)

    @property
    def active_examples(self):
        return self.packageexample_set.filter(active=True)

    @property
    def license_latest(self):
        try:
            return self.version_set.latest().license
        except Version.DoesNotExist:
            return "UNKNOWN"

    def repo_name(self):
        return re.sub(self.repo.url_regex, '', self.repo_url)

    def repo_info(self):
        return dict(
            username=self.repo_name().split('/')[0],
            repo_name=self.repo_name().split('/')[1],
        )

    def participant_list(self):

        return self.participants.split(',')

    def get_usage_count(self):
        return self.usage.count()

    def commits_over_52(self):
        cache_name = self.cache_namer(self.commits_over_52)
        value = cache.get(cache_name)
        if value is not None:
            return value
        now = timezone.now()
        commits = self.commit_set.filter(
            commit_date__gt=now - timedelta(weeks=52),
        ).values_list('commit_date', flat=True)

        weeks = [0] * 52
        for cdate in commits:
            age_weeks = (now - cdate).days // 7
            if age_weeks < 52:
                weeks[age_weeks] += 1

        value = ','.join(map(str, reversed(weeks)))
        cache.set(cache_name, value)
        return value

    def fetch_pypi_data(self, *args, **kwargs):
        # Get the releases from pypi
        if self.pypi_url.strip() and self.pypi_url != "http://pypi.python.org/pypi/":

            url = "https://pypi.python.org/pypi/{0}/json".format(self.pypi_name)
            response = requests.get(url)
            if settings.DEBUG:
                if response.status_code not in (200, 404):
                    print("BOOM!")
                    print(self, response.status_code)
            if response.status_code == 404:
                if settings.DEBUG:
                    print("BOOM!")
                    print(self, response.status_code)
                return False
            release = json.loads(response.content)
            info = release['info']

            version, created = Version.objects.get_or_create(
                package=self,
                number=info['version']
            )

            # add to versions
            license = info['license']
            if not info['license'] or not license.strip() or 'UNKNOWN' == license.upper():
                for classifier in info['classifiers']:
                    if classifier.strip().startswith('License'):
                        # Do it this way to cover people not quite following the spec
                        # at
                        # http://docs.python.org/distutils/setupscript.html#additional-meta-data
                        license = classifier.strip().replace('License ::', '')
                        license = license.replace('OSI Approved :: ', '')
                        break

            if license and len(license) > 100:
                license = "Other (see http://pypi.python.org/pypi/%s)" % self.pypi_name

            version.license = license

            # version stuff
            try:
                url_data = release['urls'][0]
                version.downloads = url_data['downloads']
                version.upload_time = url_data['upload_time']
            except IndexError:
                # Not a real release so we just guess the upload_time.
                version.upload_time = version.created

            version.hidden = info['_pypi_hidden']
            for classifier in info['classifiers']:
                if classifier.startswith('Development Status'):
                    version.development_status = status_choices_switch(classifier)
                    break
            for classifier in info['classifiers']:
                if classifier.startswith('Programming Language :: Python :: 3'):
                    version.supports_python3 = True
                    break
            version.save()

            self.pypi_description = info['description']
            self.save()
            # Calculate total downloads

            return True
        return False

    @property
    def total_downloads(self):
        total = 0
        for dl in [v.downloads for v in self.version_set.all()]:
            total += dl
        return total

    def fetch_metadata(self, fetch_pypi=True, fetch_repo=True):

        if fetch_pypi:
            self.fetch_pypi_data()
        if fetch_repo:
            self.repo.fetch_metadata(self)
        self.save()

    def save(self, *args, **kwargs):
        if not self.repo_description:
            self.repo_description = ""
        super(Package, self).save(*args, **kwargs)

    def fetch_commits(self):
        self.repo.fetch_commits(self)

    def pypi_version(self):
        version = get_pypi_version(self)
        return version

    def last_released(self):
        cache_name = self.cache_namer(self.last_released)
        version = cache.get(cache_name)
        if version is not None:
            return version
        version = get_version(self)
        cache.set(cache_name, version)
        return version

    @property
    def development_status(self):
        """ Gets data needed in API v2 calls """
        return self.last_released().pretty_status

    @property
    def pypi_ancient(self):
        release = self.last_released()
        if release:
            return release.upload_time < datetime.now() - timedelta(365)
        return None

    @property
    def no_development(self):
        commit_date = self.last_updated()
        if commit_date is not None:
            return commit_date < datetime.now() - timedelta(365)
        return None

    class Meta:
        ordering = ['title']
        get_latest_by = 'id'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy('package_index:package_detail',
                                         kwargs={
                                             'object_slug': self.slug
                                         })

    @property
    def last_commit(self):
        return self.commit_set.latest()


class PackageExample(BaseModel):

    package = models.ForeignKey(Package)
    title = models.CharField(_("Title"), max_length="100")
    url = models.URLField(_("URL"))
    active = models.BooleanField(
        _("Active"), default=True, help_text="Moderators have to approve links before they are provided")

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @property
    def pretty_url(self):
        if self.url.startswith("http"):
            return self.url
        return "http://" + self.url


class Commit(BaseModel):

    package = models.ForeignKey(Package)
    commit_date = models.DateTimeField(_("Commit Date"))
    commit_hash = models.CharField(
        _("Commit Hash"), help_text="Example: Git sha or SVN commit id", max_length=150, blank=True, default="")

    class Meta:
        ordering = ['-commit_date']
        get_latest_by = 'commit_date'

    def __unicode__(self):
        return "Commit for '%s' on %s" % (self.package.title, unicode(self.commit_date))

    def save(self, *args, **kwargs):
        # reset the last_updated and commits_over_52 caches on the package
        package = self.package
        cache.delete(package.cache_namer(self.package.last_updated))
        cache.delete(package.cache_namer(package.commits_over_52))
        self.package.last_updated()
        super(Commit, self).save(*args, **kwargs)


class VersionManager(models.Manager):

    def by_version(self, *args, **kwargs):
        qs = self.get_queryset().filter(*args, **kwargs)
        return sorted(qs, key=lambda v: versioner(v.number))

    def by_version_not_hidden(self, *args, **kwargs):
        qs = self.get_queryset().filter(*args, **kwargs)
        qs = qs.filter(hidden=False)
        qs = sorted(qs, key=lambda v: versioner(v.number))
        qs.reverse()
        return qs


class Version(BaseModel):

    package = models.ForeignKey(Package, blank=True, null=True)
    number = models.CharField(_("Version"), max_length="100", default="", blank="")
    downloads = models.IntegerField(_("downloads"), default=0)
    license = models.CharField(_("license"), max_length="100")
    hidden = models.BooleanField(_("hidden"), default=False)
    upload_time = models.DateTimeField(
        _("upload_time"), help_text=_("When this was uploaded to PyPI"), blank=True, null=True)
    development_status = models.IntegerField(
        _("Development Status"), choices=STATUS_CHOICES, default=0)
    supports_python3 = models.BooleanField(_("Supports Python 3"), default=False)

    objects = VersionManager()

    class Meta:
        get_latest_by = 'upload_time'
        ordering = ['-upload_time']

    @property
    def pretty_license(self):
        return self.license.replace("License", "").replace("license", "")

    @property
    def pretty_status(self):
        return self.get_development_status_display().split(" ")[-1]

    def save(self, *args, **kwargs):
        self.license = normalize_license(self.license)

        # reset the latest_version cache on the package
        cache_name = self.package.cache_namer(self.package.last_released)
        cache.delete(cache_name)
        get_version(self.package)

        # reset the pypi_version cache on the package
        cache_name = self.package.cache_namer(self.package.pypi_version)
        cache.delete(cache_name)
        get_pypi_version(self.package)

        super(Version, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s: %s" % (self.package.title, self.number)

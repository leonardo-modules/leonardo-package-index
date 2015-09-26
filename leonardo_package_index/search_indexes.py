from haystack import indexes, fields
from .models import Package, Category


class PackageIndex(indexes.SearchIndex, indexes.Indexable):

    """
    Index for Package objects
    """

    text = fields.CharField(document=True, use_template=True)

    title = fields.CharField(model_attr="title")
    slug = fields.CharField(model_attr="slug")
    repo_description = fields.CharField(model_attr="repo_description")
    repo_url = fields.CharField(model_attr="repo_url")
    pypi_url = fields.CharField(model_attr="pypi_url")
    pypi_description = fields.CharField(model_attr="pypi_description")
    documentation_url = fields.CharField(model_attr="documentation_url")

    last_fetched = fields.DateTimeField(model_attr='last_fetched', null=True)

    def get_model(self):
        return Package

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def get_updated_field(self):
        return "last_fetched"


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):

    """
    Index for Category objects
    """

    text = fields.CharField(document=True, use_template=True)

    title = fields.CharField(model_attr="title")
    slug = fields.CharField(model_attr="slug")
    description = fields.CharField(model_attr="description")
    title_plural = fields.CharField(model_attr="title_plural")

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


from django.template.response import SimpleTemplateResponse

from leonardo_package_index.models import Category


def category_list(request):
    object_list = Category.objects.all()
    return SimpleTemplateResponse('category/list.html',
                                  {
                                      'object_list': object_list,
                                      'request': request,

                                  }
                                  )


def category_detail(request, object_slug):
    object = Category.objects.get(
        slug=object_slug)
    return SimpleTemplateResponse('category/detail.html',
                                  {
                                      'request': request,
                                      'category': object,
                                  }
                                  )

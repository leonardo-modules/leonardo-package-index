
from django.template.response import SimpleTemplateResponse

from leonardo_package_index.models import Package


def package_list(request):
    object_list = Package.objects.all()
    return SimpleTemplateResponse('packages/list.html',
                                  {
                                      'request': request,
                                      'object_list': object_list,
                                  }
                                  )


def package_detail(request, object_slug):
    object = Package.objects.get(
        slug=object_slug)
    return SimpleTemplateResponse('packages/detail.html',
                                  {
                                      'request': request,
                                      'package': object,
                                  }
                                  )

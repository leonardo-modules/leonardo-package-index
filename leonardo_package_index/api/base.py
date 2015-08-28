
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings
from feincms.views.decorators import standalone


class BaseViewSet(viewsets.ReadOnlyModelViewSet):

    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.

    Support for custom serializer class for list and create action.

    """

    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return getattr(self,
                           "serializer_class_list",
                           self.serializer_class)
        if self.action in ["create", "update"]:
            return getattr(self,
                           "serializer_class_create",
                           self.serializer_class)
        return self.serializer_class

    @standalone
    def response(self, data):
        """just returns serialized response
        """
        return Response(data)

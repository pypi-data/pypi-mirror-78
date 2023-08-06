import django_filters
from rest_framework import viewsets
from . import mixins
from . import generics as defult_generics


class DefaultViewSet(mixins.DefaultCreateModelMixin,
                     mixins.DefaultRetrieveModelMixin,
                     mixins.DefaultUpdateModelMixin,
                     mixins.DefaultDestroyModelMixin,
                     mixins.DefaultDestroyManyModelMixin,
                     mixins.DefaultListModelMixin,
                     #  default_views.DefaultAPIView,
                     viewsets.GenericViewSet
                     ):
    """ DefaultViewSets """
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # model_class = self.get_serializer().Meta.model
    pass


class DefaultGenericViewSet(
    viewsets.ViewSetMixin, 
    defult_generics.DefaultGenericAPIView
    ):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass

# class OpRefDestroyViewSet(mixins.DefaultCreateModelMixin,
#                           mixins.DefaultRetrieveModelMixin,
#                           mixins.DefaultUpdateModelMixin,
#                           mixins.CheckRefDestroyModelMixin,
#                           mixins.DefaultListModelMixin,
#                           viewsets.GenericViewSet):
#     """ DefaultViewSets """
#     filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)



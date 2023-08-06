from rest_framework import generics
from .views import DefaultAPIView
from . import views as default_views


class DefaultGenericAPIView(default_views.DefaultAPIView, generics.GenericAPIView):

    pass

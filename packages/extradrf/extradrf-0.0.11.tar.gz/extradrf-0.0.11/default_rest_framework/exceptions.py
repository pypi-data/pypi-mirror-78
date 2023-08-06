import math

from django.http import JsonResponse
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from rest_framework import status
from rest_framework import exceptions
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class DefaultPermissionDenied(exceptions.APIException):
    status_code = status.HTTP_100_CONTINUE
    default_detail = _('test You do not have permission to perform this action.')
    default_code = 'test permission_denied'
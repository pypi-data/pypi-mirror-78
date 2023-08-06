from rest_framework.response import Response
from rest_framework import status
# from django.conf import settings
import os
# APP_NAME = os.path.dirname(os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__)))).split(os.sep)[-1]



class DefaultResponse(Response):

    default_header = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        # 'From': settings.APP_NAME
    }

    def __init__(self, data=None, status=status.HTTP_200_OK,
                 template_name=None, headers=None,
                 exception=False, content_type=None, code=True, msg="ok"):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super().__init__(None, status=status)

        self.data = {
            "code": code,
            "msg": msg,
            "results": data
        }
        if headers:
            self.default_header.update(headers)
            # print(self.default_header)
        for name, value in self.default_header.items():
            self[name] = value


FailedDefaultResponse = lambda msg: DefaultResponse(code=False, msg=msg)
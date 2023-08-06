from rest_framework import pagination
from rest_framework.response import Response
from .response import DefaultResponse

#custom reps_body
# 校验失败格式：
""" 
{
    "code": False,
    "msg": "fail",
    "results": {
        "name": [
            "模块管理 with this 模块名称 already exists."
        ]
    }
}
"""


class DefaultPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    code = True
    msg = "ok"

    def get_paginated_response(self, data):
        return DefaultResponse({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'data': data
        }, code=self.code, msg=self.msg)


class RoomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'results': data
        })


class LinkHeaderPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data, code=True):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        if next_url is not None and previous_url is not None:
            link = '<{next_url}>; rel="next", <{previous_url}>; rel="prev"'
        elif next_url is not None:
            link = '<{next_url}>; rel="next"'
        elif previous_url is not None:
            link = '<{previous_url}>; rel="prev"'
        else:
            link = ''

        link = link.format(next_url=next_url, previous_url=previous_url)
        headers = {'Link': link} if link else {}

        return Response(data, headers=headers)

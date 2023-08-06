# -*- coding:utf-8 -*-

import json
import urllib
import time
import logging
import threading
from datetime import datetime
import requests
from operator import methodcaller
from functools import partialmethod
from requests import exceptions

request_exceptions = (
    exceptions.ReadTimeout,
    exceptions.RequestException,
    exceptions.RetryError,
    exceptions.SSLError,
    exceptions.Timeout,
    exceptions.TooManyRedirects,
    exceptions.UnrewindableBodyError,
    exceptions.URLRequired,
    exceptions.StreamConsumedError
)


class Request(object):

    default_url = "http://www.baidu.com"
    default_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZG9tYWluX25hbWUiOiJzeXN0ZW0tZG9tYWluIiwiZG9tYWluX2lkIjoxLCJzeXN0ZW1fYWRtaW4iOnRydWUsIm1vZHVsZXMiOlt7ImlkIjoxMjgsIm5hbWUiOiJpcCIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMTcsIm5hbWUiOiJkYXRhZGljdCIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMjMsIm5hbWUiOiJpbmZyYXN0cnVjdHVyZSIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMTgsIm5hbWUiOiJkYXRhY2VudGVyIiwicmVhZCI6dHJ1ZSwid3JpdGUiOnRydWV9LHsiaWQiOjEyNywibmFtZSI6IklTUCIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMTUsIm5hbWUiOiJvcmNoZXN0cmF0aW9uWWFuZyIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMTYsIm5hbWUiOiJsZWFmTWFuYWdlciIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMjksIm5hbWUiOiJncm91cCIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMjUsIm5hbWUiOiJyZXNvdXJjZSIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMzIsIm5hbWUiOiJ1c2VyIiwicmVhZCI6dHJ1ZSwid3JpdGUiOnRydWV9LHsiaWQiOjEyMCwibmFtZSI6ImlwTWFuYWdlciIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMjYsIm5hbWUiOiJoZWF0QmVhdEdyb3VwIiwicmVhZCI6dHJ1ZSwid3JpdGUiOnRydWV9LHsiaWQiOjEyMSwibmFtZSI6Im1hbmFnZXJjZW50ZXIiLCJyZWFkIjp0cnVlLCJ3cml0ZSI6dHJ1ZX0seyJpZCI6MTMwLCJuYW1lIjoib3JjaGVzdHJhdGlvbkluZm8iLCJyZWFkIjp0cnVlLCJ3cml0ZSI6dHJ1ZX0seyJpZCI6MTMxLCJuYW1lIjoiaXNwbWFuYWdlciIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMjQsIm5hbWUiOiJ1c2VybWFuYWdlciIsInJlYWQiOnRydWUsIndyaXRlIjp0cnVlfSx7ImlkIjoxMjIsIm5hbWUiOiJkb21haW4iLCJyZWFkIjp0cnVlLCJ3cml0ZSI6dHJ1ZX0seyJpZCI6MTE5LCJuYW1lIjoibmV0RWxlbWVudE1hbmFnZXIiLCJyZWFkIjp0cnVlLCJ3cml0ZSI6dHJ1ZX0seyJpZCI6MTMzLCJuYW1lIjoib3JjaGVzdHJhdGlvbk1hbmFnZXIiLCJyZWFkIjp0cnVlLCJ3cml0ZSI6dHJ1ZX1dLCJleHAiOjE1NzY3MzE3MzgsImlzcyI6ImlrZ2xvYmFsLmluYyJ9.JWfcCc8GzBFtwzMIVdFWD7NPq1-D9BpO0cOe3uN_gl0"
    }

    def __init__(self, methods='get', url=None, headers=None, params=None, data=None, max_retries=1):
        self.methods = methods
        if headers:
            self.default_headers.update(headers)
        # self.default_headers.update(
        #     headers) if headers else self.default_headers
        self._headers = self.default_headers
        self._url = url if url else self.default_url
        self.params = params
        self.data = data
        self._max_retries = max_retries

    @property
    def url(self):
        return self._url

    @property
    def headers(self):
        return self._headers

    @property
    def max_retries(self):
        return self._max_retries

    def action(self, method="get"):
        error = None
        for _ in range(self.max_retries):
            try:
                # print(self.params, self.data, self.url, self.headers)
                result = getattr(requests, method)(
                    url=self.url, params=self.params, data=json.dumps(self.data), headers=self.headers)
            except request_exceptions as e:
                error = e
                continue
            except Exception as e:
                error = e
                continue
            else:
                return result
        raise error

    get = partialmethod(action, "get")
    post = partialmethod(action, "post")
    put = partialmethod(action, "put")
    patch = partialmethod(action, "patch")
    delete = partialmethod(action, "delete")
    get_default_url = partialmethod(get, default_url)



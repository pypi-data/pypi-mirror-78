# -*- coding: utf-8 -*-
import os
import datetime
from collections import namedtuple
import os
import jwt
import random
import time
import base64
import json
from functools import wraps
from rest_framework.authentication import BaseAuthentication, get_authorization_header, exceptions
from django.contrib.auth import get_user_model

User = get_user_model()

# 生成非对称秘钥
""" 
private_key = "/srv/web_develop/vpp_agent_dev/agent/source/app/keys/app.rsa"     # openssl genrsa -out app.rsa keysize
public_key  = "/srv/web_develop/vpp_agent_dev/agent/source/app/keys/app.rsa.pub" # openssl rsa -in app.rsa -pubout > app.rsa.pub
"""


def gen_synmetric_key(k_size=10):
    # return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=k_size))
    return "secret"


'''
标准中注册的声明 (建议但不强制使用) ：

iss: jwt签发者
sub: jwt所面向的用户
aud: 接收jwt的一方
exp: jwt的过期时间，这个过期时间必须要大于签发时间
nbf: 定义在什么时间之前，该jwt都是不可用的.
iat: jwt的签发时间
jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击
参考：
https://pyjwt.readthedocs.io/en/latest/usage.html#encoding-decoding-tokens-with-hs256

'''

EXP_DELTA = datetime.timedelta(weeks=10)
REFRESH_EXP_DELTA = datetime.timedelta(hours=12)
NBF_DELTA = datetime.timedelta(seconds=0)
LEEWAY = datetime.timedelta(seconds=10)
ASYMMETRIC_ENCRYP_ALGORITHM = 'RS256'
SYMMETRIC_ENCRYP_ALGORITHM = 'HS256'
HASH_ENCRYP_ALGORITHM = 'HMAC'
VERIFY_CLAIMS = ['signature', 'exp', 'nbf', 'iat']
REQUIRED_CLAIMS = ['exp', 'iat', 'nbf']

'''
对称加密
'''


class Synmetric():
    PUBLIC_KEY = gen_synmetric_key()
    SECRET = "shen"


class JWTErrorCode():
    msg_dict_10021 = {"errcode": "10021", "errmsg": "Authorization required"}
    msg_dict_10022 = {"errcode": "10022",
                      "errmsg": "Invalid JWT header, Unsupported authorization type"}
    msg_dict_10023 = {"errcode": "10023",
                      "errmsg": "Invalid JWT header, Token missing"}
    msg_dict_10024 = {"errcode": "10024",
                      "errmsg": "Invalid JWT header, Token contains spaces"}
    msg_dict_10025 = {"errcode": "10025",
                      "errmsg": "Authorization Required,Request does not contain an access token"}
    msg_dict_10027 = {"errcode": "10027", "errmsg": "Expired Token: "}


def gen_sth_for_kong():
    exp_time = int(time.time()) + 60*60*24*7
    payload = {
        'exp': exp_time,
        'iss': 'ik',
    }
    return payload, Synmetric.PUBLIC_KEY


def generate_jwt(user):
    exp_time = int(time.time()) + 60*60*24*7
    payload = {
        'exp': exp_time,
        'iss': 'ik',
        'user_id': user.get("id"),
    }
    token = jwt.encode(payload, Synmetric.PUBLIC_KEY,
                       SYMMETRIC_ENCRYP_ALGORITHM).decode("utf-8")
    return "JWT {}".format(token)


def get_payload(request):
    auth = get_authorization_header(request).split()
    if not auth:
        msg = ('缺少AUTHORIZATION或有效的验证凭证')
        raise exceptions.AuthenticationFailed(msg)
    if len(auth) == 1:
        msg = ('无效的token头，缺少有效验证凭证')
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = ('无效的token头， Token字符串内不能包括空格')
        raise exceptions.AuthenticationFailed(msg)
    contents = auth[1].decode().split(".")
    payload = base64.decodestring(contents[1].encode())
    return json.loads(payload.decode())


class NoNeedAuthentication(BaseAuthentication):

    def authenticate(self, request):
        from django.contrib.auth.models import User
        user = User(username=request.data.get("username"))
        return user, True


class JWTAuthentication(BaseAuthentication):
    """
    JWT token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "JWT ".  For example:

    Authorization: JWT 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'JWT'
    model = None

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            msg = ('缺少AUTHORIZATION或有效的验证凭证')
            raise exceptions.AuthenticationFailed(msg)
        if auth[0].lower() != self.keyword.lower().encode():
            msg = ('缺少或无效的验证凭证前缀，且前缀和凭证之间隔一个空格')
            raise exceptions.AuthenticationFailed(msg)
        if len(auth) == 1:
            msg = ('无效的token头，缺少有效验证凭证')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = ('无效的token头， Token字符串内不能包括空格')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            res = jwt.decode(token, Synmetric.PUBLIC_KEY, algorithms=[
                             SYMMETRIC_ENCRYP_ALGORITHM])
            user_id = res.get("user_id")
            try:
                user = User.objects.get(pk=user_id)
            except:
                msg = ('token user不存在！')
                raise exceptions.AuthenticationFailed(msg)
            else:
                return (user, token)
        except jwt.ExpiredSignatureError:
            msg = ('token已过期，请重新获取token！')
            raise exceptions.AuthenticationFailed(msg)


class JWTAuthentication2(BaseAuthentication):
    """
    JWT token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "JWT ".  For example:

    Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Bearer'
    model = None

    def get_payload_data(self, request):
        """
        param :
        return:
        """
        auth = self.parse_token(request)
        token = auth[1]
        _, b64_message, _ = token.decode().split('.')
        return json.loads(self.decode64(b64_message))

    def decode64(self, s: bytes) -> str:
        s_bin = s.encode('ascii')
        s_bin += b'=' * (4 - len(s) % 4)
        return base64.urlsafe_b64decode(s_bin)

    def parse_token(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            msg = ('缺少AUTHORIZATION或有效的验证凭证')
            raise exceptions.AuthenticationFailed(msg)
        if auth[0].lower() != self.keyword.lower().encode():
            msg = ('缺少或无效的验证凭证前缀，且前缀和凭证之间隔一个空格')
            raise exceptions.AuthenticationFailed(msg)
        if len(auth) == 1:
            msg = ('无效的token头，缺少有效验证凭证')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = ('无效的token头， Token字符串内不能包括空格')
            raise exceptions.AuthenticationFailed(msg)
        return auth

    def get_info(self, request):
        auth = get_authorization_header(request).split()
        try:
            token = auth[1]
            res = jwt.decode(token, Synmetric.SECRET, algorithms=[
                             SYMMETRIC_ENCRYP_ALGORITHM])
            return res
            # try:
            #     user = User.objects.get(pk=user_id)
            # except:
            #     msg = ('token user不存在！')
            #     raise exceptions.AuthenticationFailed(msg)
            # else:
            #     return (user, token)
        except jwt.ExpiredSignatureError:
            msg = ('token已过期，请重新获取token！')
            raise exceptions.AuthenticationFailed(msg)

    def authenticate(self, request):
        auth = self.parse_token(request)

        try:
            token = auth[1]
            res = jwt.decode(token, Synmetric.SECRET, algorithms=[
                             SYMMETRIC_ENCRYP_ALGORITHM])
            return res
            # try:
            #     user = User.objects.get(pk=user_id)
            # except:
            #     msg = ('token user不存在！')
            #     raise exceptions.AuthenticationFailed(msg)
            # else:
            #     return (user, token)
        except jwt.ExpiredSignatureError:
            msg = ('token已过期，请重新获取token！')
            raise exceptions.AuthenticationFailed(msg)


if __name__ == "__main__":
    pass

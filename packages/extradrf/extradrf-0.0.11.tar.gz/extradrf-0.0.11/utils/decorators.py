# -*- coding: utf-8 -*-
# from app.ikdb.model.tianshu import Permission, User
import json
import logging
import time
# from copy import deepcopy
# from apps.common.serializer import UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from .exceptions import PasswordError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import BaseValidator
from rest_framework.exceptions import ValidationError


class IDsValidator(BaseValidator):

    def __call__(self, value):
        cleaned = self.clean(value)
        if not self.compare(cleaned, self.limit_value) or self.is_empty(cleaned):
            raise ValidationError({"ids": [
                "数据类型必须为list，内容不能为空"
            ]})

    def compare(self, a, b):
        return isinstance(a, b)

    def is_empty(self, a):
        return not bool(a)


# count func calls
class Count:
    """ 初始化Count实例 """

    def __init__(self, func):
        self.func = func
        self.num_calls = 0
        self.__name__ = func.__name__
    """ 统计wrapped函数调用次数 """

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        # ik_global.Logger.info('num of Function<{}> calls is: {}'.format(
        # self.__name__, self.num_calls))
        return self.func(*args, **kwargs)


def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        # ik_global.Logger.info('{} took {} ms'.format(
        # func.__name__, (end - start) * 1000))
        return res
    return wrapper


# def use_cache(timeout=5):
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):  # --->f
#             # ik_global.Logger.info(f.__name__)
#             cache = # ik_global.CACHE.get(f.__name__)
#             if not cache:
#                 # ik_global.Logger.info("not use cache")
#                 # ik_global.CACHE.set(f.__name__, f(
#                     # *args, **kwargs), timeout=timeout)
#             return  # ik_global.CACHE.get(f.__name__)
#             # if cache:
#             #     # ik_global.Logger.info("use_cache")
#             #     return succ_resp_json_make("ok", cache)
#             # # ik_global.Logger.info("not use cache")
#             # return f(*args, **kwargs)
#         return wrapper
#     return decorator


# def record_restart():
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if  # ik_global.nso_INSTANCE:
#                 # ik_global.RESTART_FLAG = None
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator


class Validate():

    """ 
    @classmethod
    # @api_view(['POST'])
    def user_login(cls, request, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            serializer = UserLoginSerializer(
                data=request.data)  # 带data参数，表示要校验数据
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return f(*args, **kwargs)
        return decorated_function
    """

    @classmethod
    def validate_set_node_id_post(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            schema = Schema({
                Required('masterid'): All(int, Range(min=1, max=10000)),
                Required('nodeid'): All(int, Range(min=1, max=10000)),
                # 'phone': All(str, Length(min=11, max=11)),
            })
            try:
                schema(json_data)
                print("valiate ok")
                # raise AssertionError('MultipleInvalid not raised')
            except MultipleInvalid as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            return f(*args, **kwargs)
        return decorated_function

    @classmethod
    def validate_exec_system_cmd(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            schema = Schema({
                Required('cmd'): All(str),
            })
            try:
                schema(json_data)
                print("valiate ok")
                # raise AssertionError('MultipleInvalid not raised')
            except (MultipleInvalid, ) as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            return f(*args, **kwargs)
        return decorated_function

    @classmethod
    def validate_nso_start(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            # 第一层校验
            schema = Schema({
                Required('config'): All(dict),
                Required('port_id'): All(list)
            })
            try:
                schema(json_data)
                print("valiate ok")
                # raise AssertionError('MultipleInvalid not raised')
            except MultipleInvalid as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            # config字段检验
            config = json_data.get("config")
            schema2 = Schema({
                Required('arp_attr'): All(dict),
                Required('dst'): All(dict),
                Required('method'): All(str, Length(min=3, max=16)),
                Required('setting'): All(dict),
                Required('src'): All(dict),
                Required('test_args'): All(dict),
                # 'phone': All(str, Length(min=11, max=11)),
            })
            try:
                schema2(config)
                print("valiate ok")
                # raise AssertionError('MultipleInvalid not raised')
            except MultipleInvalid as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            # port_id字段检验
            # config = json_data.get("config")
            return f(*args, **kwargs)
        return decorated_function

    @classmethod
    def validate_nso_stop(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            # 第一层校验
            schema = Schema({
                # Required('config'): All(dict),
                Required('port_id'): All(list)
            })
            try:
                schema(json_data)
                print("valiate ok")
                # raise AssertionError('MultipleInvalid not raised')
            except MultipleInvalid as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            return f(*args, **kwargs)
        return decorated_function

    @classmethod
    def validate_user_post(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            schema = Schema({
                Required('name'): All(str, Length(min=1)),
                Required('passwd'): All(str, Length(min=8, max=16)),
                Required('company'): All(str, Length(min=1)),
                Required('email'): All(str, Length(min=1)),
                Required('exp_time'): All(str),
                Required('role_id'): All(int, Range(min=1, max=2)),
                # Required('group_id'): All(int),
                Required('status'): All(int, Range(min=1, max=2)),
                'phone': All(str, Length(min=11, max=11)),
            })
            try:
                schema(json_data)
                print("valiate ok")
                # raise AssertionError('MultipleInvalid not raised')
            except MultipleInvalid as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            return f(*args, **kwargs)
        return decorated_function

    @classmethod
    def validate_user_del(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            # ids = json_data.get("ids", None)
            # if ids is None:
            #     return err_resp_json_make(errcode=FAIL, extra_errmsg="ids can't be empty or keyname must be 'ids'", result='')
            schema = Schema({
                Required('ids'): All(list)
            })
            try:
                schema(json_data)
                print("valiate ok")
                # raise AssertionError('MultipleInvalid not raised')
            except MultipleInvalid as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            return f(*args, **kwargs)
        return decorated_function

    @classmethod
    def validate_user_login(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            schema = Schema({
                Required('name'): All(str),
                Required('passwd'): All(str),
            })
            try:
                schema(json_data)
                print("valiate ok")
                # raise AssertionError('MultipleInvalid not raised')
            except MultipleInvalid as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            return f(*args, **kwargs)
        return decorated_function
        # return validate_user_del()

    @classmethod
    def router_del(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            uuids = json_data.get("uuids", None)
            if not uuids:
                return err_resp_json_make(errcode=FAIL, extra_errmsg="uuids can't be None or empty", result='')
            schema = Schema({
                Required('uuids'): All(list)
            })
            try:
                schema(json_data)
                print("valiate ok")
                # raise AssertionError('MultipleInvalid not raised')
            except MultipleInvalid as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            return f(*args, **kwargs)
        return decorated_function

    @classmethod
    def router_put(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # args
            args_dict = request.args.to_dict()
            schema = Schema({
                Required('room_uuid'): All(str),
                Required('router_uuid'): All(str)
            })
            try:
                schema(args_dict)
                print("valiate ok")
            except MultipleInvalid as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            if not args_dict.get("room_uuid") or not args_dict.get("router_uuid"):
                return err_resp_json_make(errcode=FAIL, extra_errmsg="put_router fail, room_uuid and router_uuid can’t be null")

            # body
            json_data = request.get_json()
            schema = Schema({
                Required('alias'): All(str),
                Required('ip'): All(str),
                Required('port'): All(int),
                Required('username'): All(str),
                Required('password'): All(str),
                Required('manufacturer'): All(str)
            })
            try:
                schema(json_data)
                print("valiate ok")
                # raise AssertionError('MultipleInvalid not raised')
            except MultipleInvalid as e:
                print(str(e))
                return err_resp_json_make(errcode=FAIL, extra_errmsg=str(e), result='')
            return f(*args, **kwargs)
        return decorated_function


# def permission_required(permission):
#     def decorator(f):
#         @wraps(f)
#         def _deco(*args, **kwargs):
#             try:
#                 # if not current_user.can(permission):
#                 #     abort(403)
#                 _user = get_user_from_token()
#                 if not _user.can(permission):
#                     return err_resp_json_make(extra_errmsg='token_user not permitted', result="")
#             except Exception as e:
#                 # ik_global.Logger.info(str(e))
#                 return err_resp_json_make(extra_errmsg='permission_required error ', result=str(e))
#             return f(*args, **kwargs)
#         return _deco
#     return decorator


# def get_user_from_token():
#     _ident = _request_ctx_stack.top.current_identity
#     _user = User.one(id=_ident.id)
#     return _user


# def admin_required(f):
#     return permission_required(Permission.ADMINISTER)(f)


'''
def add_log_first(action_):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                content = json.dumps(request.get_json(), ensure_ascii=False)
                user_name = current_identity.username
                log = {
                    "email": user_name,
                    'action':action_,
                    "path": request.path,
                    "message": 'success',
                    "result": 1,
                    "content": content}
                ikdb.add_operation_log(# ik_global.dbp, log)
            except Exception as e:
                LOG.exception(e)
                pass
            result = f(*args, **kwargs)
            return result
        return decorated_function
    return decorator
'''

'''
def add_log(action_, remove_field=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = None
            message = ''
            json_result = deepcopy(request.get_json())
            if remove_field:
                for item in remove_field:
                    json_result.pop(item)
            content = json.dumps(json_result, ensure_ascii=False)
            user_name = current_identity.username
            try:
                result = f(*args, **kwargs)
            except PasswordError as e:
                message = e.message
                content = ''
                raise
            except Exception as e:
                message = e.message
                raise
            finally:
                try:
                    log = {
                        "email": user_name,
                        'action': action_,
                        "path": request.path,
                        "content": content}
                    if result:
                        resp = json.loads(result)
                        if resp.get('status_code') == SUCCESS:
                            log.update({"message": 'success', "result": 1})
                        else:
                            log.update(
                                {"message": resp.get('message'), "result": 2})
                    else:
                        log.update({"message": message, "result": 2})
                    # ikdb.add_operation_log(# ik_global.dbp, log)
                except Exception as e:
                    LOG.exception(e)
                    pass
            return result
        return decorated_function
    return decorator
'''

'''
def login_log(action_):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = None
            message = 'success'
            request_data = request.get_json()
            user_name = ''
            if current_identity and current_identity.username:
                user_name = current_identity.username
            else:
                user_name = request_data.get('username', '')
            try:
                result = f(*args, **kwargs)
            except Exception as e:
                message = e.description if isinstance(
                    e, JWTError) else e.messsage
                raise
            finally:
                try:
                    if request.headers.getlist("X-Forwarded-For"):
                        login_ip = request.headers.getlist(
                            "X-Forwarded-For")[0]
                    else:
                        login_ip = request.remote_addr
                    log = {
                        "email": user_name,
                        'action': action_,
                        "login_ip": login_ip,
                        "message": message}
                    # ikdb.add_login_log(# ik_global.dbp, log)
                except Exception as e:
                    LOG.exception(e)
                    pass
            return result
        return decorated_function
    return decorator
'''

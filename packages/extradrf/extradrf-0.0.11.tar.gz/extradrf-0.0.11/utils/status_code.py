# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from flask import json
from flask import current_app

# old status
SUCCESS = 200  # all success code
FAIL = 500
TIMEOUT = 3


# client error code
UNAUTHORIZED = 401
FORBIDDEN = 403


# custommized client error code
NOT_EXIST = 4001
WRONG_PARAMETER = 4002


# server error
INTERNAL_ERROR = 500


# database error code start from 6000
FOREIGN_KEY_CONSTRAINT = 6000


INCONSISTENCY = 6100  # 数据不一致


# ddos error code start from 7000
DDOS_NOT_READY = 7000


STATUS_CODE_MSG = {
    SUCCESS: 'Ok',
    FAIL: 'Fail',
    TIMEOUT: 'Timeout',
    UNAUTHORIZED: 'unauthorized',
    FORBIDDEN: 'Forbidden',
    FOREIGN_KEY_CONSTRAINT: 'Foreign key constraint',
    DDOS_NOT_READY: 'DDoS Not Ready',

}

""" 自定义Response """
# class JSONResponse(Response):
#     @classmethod
#     def force_type(cls, rv, environ=None):
#         if isinstance(rv, dict):
#             rv = jsonify(rv)
#         return super(JSONResponse, cls).force_type(rv, environ)


# current_app.response_class = JSONResponse


""" custom header """


def custom_headers(errcode="", extra_errmsg='', result='', header_code="201", header_list=[('X-Request-Id', '100')]):
    
    # response body, header code, header field
    return err_resp_json_make(errcode=errcode, extra_errmsg=extra_errmsg, result=''), str(header_code), header_list
# {'headers': [1, 2]}, "201 custom_headers", [('X-Request-Id', '100'),('user_id', '11')]


def err_resp_json_make(errcode=FAIL, extra_errmsg='', result=''):

    # errmsg = None
    # if not extra_errmsg:
    #     errmsg = STATUS_CODE_MSG.get(errcode, '')
    # else :
    #     errmsg = extra_errmsg

    rsp_web_dict = {"status_code": errcode,
                    "message": extra_errmsg, "result": result}
    rsp_web_json = json.dumps(rsp_web_dict)

    return rsp_web_json


def succ_resp_json_make(extra_errmsg='', result=''):
    return err_resp_json_make(SUCCESS, extra_errmsg, result)

# def err_resp_json(errcode, extra_errmsg='',result=''):

#     # errmsg = None
#     # if not extra_errmsg:
#     #     errmsg = STATUS_CODE_MSG.get(errcode, '')
#     # else :
#     #     errmsg = extra_errmsg
#     data_dict = {}
#     data_dict["result"]={"node_ipaddr":data_dict.pop("node_ipaddr"),"node_connect_result":"vpp ok"}
#     data_dict["status_code"]=SUCCESS
#     data_dict["message"]="vpp_connnect ok"
#     return json.dumps(data_dict)

#     rsp_web_dict = {"status_code": errcode, "message": extra_errmsg, "result":result}
#     rsp_web_json = json.dumps(rsp_web_dict)

#     return rsp_web_json

# def succ_resp_json(extra_errmsg='',result=''):
#     return err_resp_json(SUCCESS, extra_errmsg, result)

import re
from rest_framework.exceptions import ErrorDetail, ValidationError


def mobile_validate(value):
    mobile_re = re.compile(
        r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


def file_size_validate(value):
    """
    param :
    return:
    """
    #print(value)
    return value


def int_validate(value):
    #print(value)
    assert isinstance(value, int), ("field type must be int")


def action_validate(value):
    """
    param :
    return:
    """
    # assert (value == "add_ref" and value == "del_ref"), (
    #     "add_ref or del_ref not found in action field")
    if not value == "add_ref" and not value == "del_ref":
        raise Exception("add_ref or del_ref not found in action field")


def owner_validator(value):
    """
    param :
    return:
    """
    if not isinstance(value, dict):
        raise ValidationError('type of owner <{}> must be dict'.format(value))
    for k, v in value.items():
        if not isinstance(k, str):
            raise ValidationError(
                "type of owner <{}>'s key must be str".format(value))
        try:
            if not isinstance(int(k), int):
                raise ValidationError(
                    "convert type of k <{}> to int fail".format(k))
        except Exception as e:
            raise ValidationError(str(e))
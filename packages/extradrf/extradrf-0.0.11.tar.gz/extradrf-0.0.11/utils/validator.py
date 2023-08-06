from rest_framework import serializers
from utils.ik_util import get_file_size_by_mbytes
from django.conf import settings
import re
from rest_framework.exceptions import ValidationError


def mobile_validate(value):
    mobile_re = re.compile(
        r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


def file_validate(value):
    """
    param :
    return:
    """
    # print(value)
    return value


def int_validate(value):
    # print(value)
    assert isinstance(value, int), ("field type must be int")


def validate_file_size(file):
    file_size = get_file_size_by_mbytes(file)
    # print(file_size)
    if file_size > settings.UPLOAD_FILE_MAX_SIZE:
        raise serializers.ValidationError(
            "合同附件({})大小不能大于{}M".format(file.name, settings.UPLOAD_FILE_MAX_SIZE))


def validate_multi_file_size(files):
     # files = self.get_files()
    if not files:
        # print("files not found")
        raise serializers.ValidationError("没有上传附件")
    for _, file in files.items():
        file_size = get_file_size_by_mbytes(file)
        # print(file_size)
        if file_size > settings.UPLOAD_FILE_MAX_SIZE:
            raise serializers.ValidationError(
                "合同附件({})大小不能大于{}M".format(file.name, settings.UPLOAD_FILE_MAX_SIZE))


def FileValidator(value):
    # if not value:
    #     raise serializers.ValidationError("没有上传附件")
    validate_file_size(value)
    return value

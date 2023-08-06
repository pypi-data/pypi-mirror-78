from rest_framework import serializers
from . import mixins
from django.db import transaction


class RefFieldMixin:

    def update(self, instance, validated_data):
        if "referenced" in validated_data:
            raise serializers.ValidationError("更新接口携带数据不能包含referenced字段")
        return super().update(instance, validated_data)


class OperateRefResourceOwnerModelMixin:
    """ data structure
    {
        "ids": [1, 2] # operation obj id
        "action": "add_ref" # add_ref or del_ref
        "referenced": {
            "isp_manager_tbl_line_manager_12": 1
        }
    }
    """

    def add_ref(self, validated_data):
        with transaction.atomic():
            for _id in validated_data.get("ids"):
                inst = self.Meta.model.objects.get(pk=_id)
                referenced_data = validated_data.get("referenced")
                inst.referenced.update(referenced_data)
                inst.save()

    def del_ref(self, validated_data):
        with transaction.atomic():
            for _id in validated_data.get("ids"):
                try:  # don't raise exception when del ref
                    inst = self.Meta.model.objects.get(pk=_id)
                except Exception as e:
                    # print(str(e))
                    continue
                referenced_data = validated_data.get("referenced")
                try:
                    del_keys = list(referenced_data.keys())
                    for i in del_keys:
                        try:
                            def_ref = inst.referenced.pop(i)
                        except Exception as e:
                            continue
                except Exception as e:
                    # print(str(e))
                    continue
                    # don't raise exception when del ref
                    # raise serializers.ValidationError(
                    #     "delete ref fail: {} may not exists".format(e))
                inst.save()


class DeleteManySerializer(serializers.Serializer):
    ids = serializers.ListField(label='删除id列表', required=True)

    """ 
    def validate(self, data):
        #print("validate")
        return data 
    """

    def validate_ids(self, value):
        """
        Check ids
        """
        #print("validate_ids")
        if not self.compare(value, list) or self.is_empty(value):
            raise serializers.ValidationError("数据类型必须为list，内容不能为空")
        return value

    def compare(self, a, b):
        return isinstance(a, b)

    def is_empty(self, a):
        return not bool(a)

class RetrieveInListSerializer(serializers.Serializer):
    ids = serializers.ListField(label='获取对象id列表', required=True)

    def validate_ids(self, value):
        """
        Check ids
        """
        #print("validate_ids")
        if not self.compare(value, list) or self.is_empty(value):
            raise serializers.ValidationError("获取对象id列表数据类型必须为list，内容不能为空")
        return value

    def compare(self, a, b):
        return isinstance(a, b)

    def is_empty(self, a):
        return not bool(a)


class ReferenceSerializer(serializers.ModelSerializer,
                          OperateRefResourceOwnerModelMixin):

    class Meta:
        model = ""
        # fields = ["objs"]
        fields = []

    def _validate_action(self, data):
        """
        param :
        return:
        """
        value = data.get("action")
        if value == "add_ref" or value == "del_ref":
            return value
        raise Exception("add_ref or del_ref not found in action field")

    def _validate_ids(self, data, model_class):
        """
        Check ids
        """
        #print("validate_ids")
        value = data.get("ids")
        if not self.compare(value, list) or self.is_empty(value):
            # return DefaultResponse("数据类型必须为list，内容不能为空", code=False)
            raise serializers.ValidationError("数据类型必须为list，内容不能为空")
        # check
        for i in value:
            if not model_class.objects.filter(pk=i).exists():
                # [].pop
                # continue
                raise serializers.ValidationError(
                    "id: {} not exists in {}".format(i, model_class))
        return value

    def _get_valid_ids(self, data, model_class):
        """
        Check ids
        """
        #print("validate_ids")
        value = data.get("ids")
        if not self.compare(value, list) or self.is_empty(value):
            # return DefaultResponse("数据类型必须为list，内容不能为空", code=False)
            raise serializers.ValidationError("数据类型必须为list，内容不能为空")
        # check
        exist_ids = []
        for i in value:
            if model_class.objects.filter(pk=i).exists():
                exist_ids.append(i)
                # continue
            # raise serializers.ValidationError(
            #     "id: {} not exist in {}".format(i, model_class))

        if len(exist_ids) == 0:
            raise serializers.ValidationError("ids not exist")
        return exist_ids

    def _get_valid_ids_of_add_ref(self, data, model_class):
        value = data.get("ids")
        if not self.compare(value, list) or self.is_empty(value):
            # return DefaultResponse("数据类型必须为list，内容不能为空", code=False)
            raise serializers.ValidationError("数据类型必须为list，内容不能为空")
        for i in value:
            if not model_class.objects.filter(pk=i).exists():
                raise serializers.ValidationError(
                    "id: {} not exist in {} when add_ref".format(i, model_class))

    def _validate_referenced(self, data):
        value = data.get("referenced")
        assert (isinstance(value, dict)
                ), ("type of referenced field must be dict")
        #print(value)

    def compare(self, a, b):
        return isinstance(a, b)

    def is_empty(self, a):
        return not bool(a)


class BulkOperateReferenceSerializer(ReferenceSerializer):
    """
    def_ref:
    objs: [
            {
            "ids": [1, 2] # operation obj id
            "action": "add_ref" # add_ref or del_ref
            "referenced": {
                "isp_manager_tbl_line_manager_12": 1
            }
        }
    ]
    """
    objs = serializers.ListField(label='关联的对象列表', required=True,
                                 child=serializers.DictField(label='关联对象', required=True))

    # _meta_class = None

    class Meta:
        model = None
        fields = ["objs"]

    def __init__(self, *args, **kwargs):
        # for dynamic inject model class of Meta
        self.Meta.model = kwargs.pop("meta_class")
        super(BulkOperateReferenceSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        #print("validate")
        self._bulk_validate_objs_data(data)
        return data

    def _bulk_validate_objs_data(self, _data):
        for data in _data.get("objs"):
            self._validate_action(data)
            self._validate_ids(data, model_class=self.Meta.model)
            self._validate_referenced(data)

    def save(self):
        return self.bulk_patch(self.validated_data)

    def patch(self, validated_data):
        """
        param validated_data:
        return:
        """
        #print(validated_data)
        action = validated_data.get("action")
        getattr(self, action)(validated_data)  # add ref or del ref

    def bulk_patch(self, validated_data):
        for obj_data in validated_data.get("objs"):
            self.patch(obj_data)


class BulkOperateReferenceSerializer2(ReferenceSerializer):
    """
    def_ref:
    objs: [
            {
            "ids": [1, 2] # operation obj id
            "action": "add_ref" # add_ref or del_ref
            "referenced": {
                "isp_manager_tbl_line_manager_12": 1
            }
        }，
        {
            "ids": [3, 4] # operation obj id
            "action": "del_ref" # add_ref or del_ref
            "referenced": {
                "isp_manager_tbl_line_manager_11": 1
            }
        }
    ]
    """
    objs = serializers.ListField(label='关联的对象列表', required=True,
                                 child=serializers.DictField(label='关联对象', required=True))

    class Meta:
        model = None
        fields = ["objs"]

    def __init__(self, *args, **kwargs):
        # for dynamic inject model class of Meta
        self.Meta.model = kwargs.pop("meta_class")
        super().__init__(*args, **kwargs)

    def validate(self, data):
        #print("validate")
        # self._bulk_validate_objs_data(data)
        # return data
        return self._bulk_validate_objs_data2(data)

    def _bulk_validate_objs_data(self, _data):
        for data in _data.get("objs"):
            self._validate_action(data)
            self._validate_ids(data, model_class=self.Meta.model)
            self._validate_referenced(data)

    def _bulk_validate_objs_data2(self, _data):
        for data in _data.get("objs"):
            action = self._validate_action(data)
            if action == 'add_ref':  # verify ids when add ref
                getattr(self, '_get_valid_ids_of_add_ref')(
                    data, self.Meta.model)
            self._validate_referenced(data)
        return _data

    def save(self):
        return self.bulk_patch(self.validated_data)

    def patch(self, validated_data):
        """
        param validated_data:
        return:
        """
        #print(validated_data)
        action = validated_data.get("action")
        getattr(self, action)(validated_data)  # add ref or del ref

    def bulk_patch(self, validated_data):
        with transaction.atomic():  # garantee the atmoic operation
            for obj_data in validated_data.get("objs"):
                self.patch(obj_data)

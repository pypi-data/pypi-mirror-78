
from rest_framework import status
from default_rest_framework import DefaultResponse, FailedDefaultResponse
from rest_framework.decorators import action
from .serializers import DeleteManySerializer, BulkOperateReferenceSerializer2, RetrieveInListSerializer
from rest_framework.settings import api_settings
from operator import methodcaller
import json
from django.db import transaction
import datetime
from django.db.models.query import QuerySet
from django.db.models import Q
from utils.http_service import Request
import abc


# from data_dict_app import serializer
# from extra.default_rest_framework import serializers as default_serializers

##########################atmoic mixin###########################


class AbstractRemoteAccessMixin(metaclass=abc.ABCMeta):
    """
    AbstractRemoteAccessMixin
    """
    @abc.abstractmethod
    def action(self, url, data, method):
        pass


# class OperateRefResourceOwnerModelMixin:
#     """ data structure
#     {
#         "ids": [1, 2] # operation obj id
#         "action": "add_ref" # add_ref or del_ref
#         "referenced": {
#             "isp_manager_tbl_line_manager_12": 1
#         }
#     }
#     """

#     def add_ref(self, validated_data):
#         with transaction.atomic():
#             for _id in validated_data.get("ids"):
#                 inst = self.Meta.model.objects.get(pk=_id)
#                 referenced_data = validated_data.get("referenced")
#                 inst.referenced.update(referenced_data)
#                 inst.save()

#     def del_ref(self, validated_data):
#         with transaction.atomic():
#             for _id in validated_data.get("ids"):
#                 inst = self.Meta.model.objects.get(pk=_id)
#                 referenced_data = validated_data.get("referenced")
#                 try:
#                     del_keys = list(referenced_data.keys())
#                     for i in del_keys:
#                         def_ref = inst.referenced.pop(i)
#                     # del_ref = inst.referenced.pop(
#                     #     list(referenced_data.keys())[0])
#                 except Exception as e:
#                     print(str(e))
#                     raise serializers.ValidationError(
#                         "delete ref fail: {}".format(e))
#                 inst.save()


class ORMModelMixin:
    """
    ORMModelMixin for Model common attr and method
    """
    @property
    def app_tbl_instance_id(self):
        return "_".join([self._meta.app_label, self._meta.db_table, str(self.id)])

    def __str__(self):
        return "{}".format(self.id)

    @property
    def _to_dict(self):
        field_dict = {}
        for field in self._meta.fields:
            key, value = field.get_attname(), getattr(self, field.get_attname())
            field_dict.setdefault(key, value)
        return field_dict

    def __repr__(self):
        return self._to_dict


class CreatorOwnerModelMixin:
    """
    CreatorOwnerModelMixin for Model with creator and owner field common attr and method
    """

    def add_owner(self, owner):
        # self.owner.append(owner_name)
        assert (isinstance(owner, dict)), ("add owner type must be dict")
        self.owner.update(owner)

    def del_owner(self, owner_key):
        # assert (isinstance(owner_key, str)), ("del owner_key type must be str")
        self.owner.pop(owner_key)
        pass

    def add_creator(self, creator):
        assert (isinstance(creator, dict)), ("add creator type must be dict")
        self.creator.update(creator)

    def del_creator(self, creator_key):
        # assert (isinstance(creator_key, str)
        #        ), ("del creator_key type must be str")
        self.creator.pop(creator_key)

    def update_owner(self, old_owner_name, new_owner_name):
        # self.owner.append(owner_name)
        pass

    def _field_creator_to_list(self):
        return [int(i) for i in dict(self.creator).keys()]

    def _field_owner_to_list(self):
        return [int(i) for i in dict(self.owner).keys()]

    @staticmethod
    def list_to_dict(_list, val=1):
        """
        param _list:
        return:
        """
        _field_dict = {}
        for _id in _list:
            _field_dict.setdefault(str(_id), val)
        return _field_dict


class TaskModelMixin:

    def create_task(self, kwargs):
        # print("create_task")
        return

    def del_task(self, kwargs):
        # del task by contractid
        # check delete_many by instance is querysets or not
        # print("del_task")
        return

    def bulk_del_task(self, kwargs):
        # del task by contractid
        # check delete_many by instance is querysets or not
        # print("bulk_del_task")
        return
        # print(type(kwargs))
        if isinstance(kwargs, QuerySet):
            for instance in list(kwargs):
                pass
                # print("del task by contractid: {}".format(instance.id))
            return
        # print(kwargs)
        # print("del task by contractid: {}".format(kwargs.get("pk")))
        pass
        # if create task fail raise exception
        # if not serializer:
        #     raise Exception("no found")


class OperateRemoteRefMixin:

    def operate_remote_ref(self, *args, **kwargs):
        """
        add_or_del_remote_ref
        """
        raise NotImplementedError("method must be implemented")

    def bulk_operate_remote_ref(self, *args, **kwargs):
        """
        bulk_add_or_del_remote_ref
        """
        raise NotImplementedError("method must be implemented")


class DefaultOperateRemoteRefMixin(OperateRemoteRefMixin):

    def operate_remote_ref(self, instance, add_or_del_remote_ref, *args, **kwargs):
        """ 
        param: instance
        param: add_or_del_remote_ref
        """
        """ 
        {
            "ids": [1, 2] # operation obj id
            "action": "add_ref" # add_ref or del_ref
            "referenced": {
                "isp_manager_tbl_line_manager_12": 1
            }
        } 
        """
        ids = [instance.logic_ap_id, instance.phyical_ap_id] if instance.logic_ap_id != instance.phyical_ap_id else [
            instance.logic_ap_id]
        data = {
            "ids": ids,
            "action": "add_ref" if add_or_del_remote_ref else "del_ref",
            "referenced": {
                instance.app_tbl_instance_id: add_or_del_remote_ref
            }
        }
        action = {
            "url": conf.OPERATE_REMOTE_REF_URL,
            "data": data,
            "method": "patch",
            "headers": kwargs.get("headers")
        }
        self.do_action(**action)

    def bulk_operate_remote_ref(self, instance_list, add_or_del_remote_ref, *args, **kwargs):
        """ 
        {
            "objs": [
                {
                    "ids": [
                        1,3
                    ],
                    "action": "del_ref",
                    "referenced": {
                        "isp_manager_tbl_line_manager_22": 0
                    }
                }
            ]
        } 
        """
        assert (isinstance(instance_list, list)
                ), ("type of <{}> must be list, but got {}".format(instance_list, type(instance_list)))
        objs_list = []
        for instance in instance_list:
            ids = [instance.logic_ap_id, instance.phyical_ap_id] if instance.logic_ap_id != instance.phyical_ap_id else [
                instance.logic_ap_id]
            obj = {
                "ids": ids,
                "action": "add_ref" if add_or_del_remote_ref else "del_ref",
                "referenced": {
                    instance.app_tbl_instance_id: instance.app_tbl_instance_id_cn
                }
            }
            objs_list.append(obj)

        data = {"objs": objs_list}
        action = {
            "url": conf.OPERATE_REMOTE_REF_URL,
            "data": data,
            "method": "patch",
            "headers": kwargs.get("headers")
        }
        self.do_action(**action)


class RemoteAccessMixin:

    def do_action(self, url, data, method, headers=None):
        """
        param :
        return:
        """
        assert (headers is not None), ("do_action must set http headers")
        req = Request(
            url=url,
            data=data,
            headers=headers
        )
        try:
            res = methodcaller(method)(req)
        except Exception as e:
            # print(str(e))
            raise Exception(str(e))
        text = json.loads(res.text)
        if not text.get("code"):
            raise Exception(str(text))
            # raise Exception(text.get("msg"))
        return res


class DefaultCreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return DefaultResponse(code=False, msg=str(serializer.errors))
        try:
            self.perform_create(serializer)
        except Exception as e:
            return DefaultResponse(code=False, msg=str(e))
        headers = self.get_success_headers(serializer.data)
        return DefaultResponse(serializer.data, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class DefaultDestroyModelMixin:

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            # print(str(e))
            # return FailedDefaultResponse(msg=str(e))
            return DefaultResponse("删除成功", status=status.HTTP_200_OK)
        try:
            self.perform_destroy(instance)
        except Exception as e:
            # print(str(e))
            return FailedDefaultResponse(msg="删除失败: {}".format(str(e)))
            # return DefaultResponse(msg="删除失败: {}".format(str(e)), code=False, status=status.HTTP_200_OK)
        return DefaultResponse("删除成功", status=status.HTTP_200_OK)


class DefaultDestroyManyModelMixin:

    def perform_destroy_many(self, ids):
        queryset = self.get_queryset()
        querysets = queryset.filter(pk__in=ids)
        if len(list(querysets)) <= 0:
            raise Exception("批量删除失败, 查询数据为：{}".format(list(querysets)))
            # return DefaultResponse(status=status.HTTP_200_OK, code=False, msg="批量删除失败, 查询数据为：{}".format(list(querysets)))
        querysets.delete()

    @action(methods=['DELETE'], detail=False)
    def delete_many(self, request, format=None):
        ids = request.data.get('ids')
        # validate field and field type
        serializer = DeleteManySerializer(data=request.data)
        if not serializer.is_valid():
            return FailedDefaultResponse(msg=str(serializer.errors))
            # return DefaultResponse(code=False, msg=str(serializer.errors))
        try:
            self.perform_destroy_many(ids)
        except Exception as e:
            return FailedDefaultResponse(msg="批量删除失败: {}".format(str(e)))
        return DefaultResponse("批量删除成功", status=status.HTTP_200_OK)


class DefaultRetrieveInListModelMixin:

    def perform_retrieve_in_list(self, ids):
        querysets = self.get_queryset().filter(pk__in=ids)
        return querysets

    @action(methods=["POST"], detail=False)
    def retrieve_in_list(self, request, format=None):
        ids = request.data.get('ids')
        serializer = RetrieveInListSerializer(data=request.data)
        if not serializer.is_valid():
            return FailedDefaultResponse(msg=str(serializer.errors))
        try:
            qs = self.perform_retrieve_in_list(ids)
            serializer = self.get_serializer(qs, many=True)
            # TODO 提高序列号性能
            # serializer = serializer.NetElementManagerSerializer2(qs, many=True)
        except Exception as e:
            return FailedDefaultResponse(msg="按id列表查询失败: {}".format(str(e)))
        return DefaultResponse(serializer.data)


class DefaultListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except Exception as e:
            # print(str(e))
            return DefaultResponse(msg="查询失败: {}".format(str(e)), code=False, status=status.HTTP_200_OK)

        # 查询所有
        if not request.query_params.get("page") or not request.query_params.get("page_size"):
            try:
                serializer = self.get_serializer(queryset, many=True)
            except Exception as e:
                # print(str(e))
                return DefaultResponse(msg="查询失败: {}".format(str(e)), code=False, status=status.HTTP_200_OK)
            return DefaultResponse(serializer.data)
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # print(serializer.data)
            return self.get_paginated_response(serializer.data)


class DefaultRetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DefaultResponse(serializer.data)


class DefaultUpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return DefaultResponse(code=False, msg=str(serializer.errors))
        try:
            self.perform_update(serializer)
        except Exception as e:
            return DefaultResponse(code=False, msg=str(e))

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return DefaultResponse(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class OperateCreatorOwnerFieldMixin:
    """  """

    def add_creator_owner_field(self, validated_data):
        """
        add creator and owner to validated_data
        param :
        return:
        """
        # jwt_obj = self.context.get("request").data.get("jwt")
        jwt_obj = self.context.get("request").jwt
        validated_data.update({
            "creator": {jwt_obj.domain_id: 1}
        })
        return validated_data

    def get_queryset(self):
        """

        super get_queryset and add query data filter by creator or owner
        param :
        return:
        """
        queryset = super().get_queryset()
        # jwt_info = self.request.jwt
        jwt_info = self.request.jwt
        domain_id = jwt_info.domain_id
        internal = jwt_info.message.get('internal')
        if jwt_info.system_admin:
            return queryset
        if internal:
            filter_query_set = queryset.filter(Q(resource_type__in=[self.model_class.INTERNAL_RESOURCE_TYPE, self.model_class.EXTERNAL_RESOURCE_TYPE]) | Q(
                creator__has_key=str(domain_id)) | Q(owner__has_key=str(domain_id)))
        else:
            filter_query_set = queryset.filter(
                Q(creator__has_key=str(domain_id)) | Q(owner__has_key=str(domain_id)))
        # filter_query_set = queryset
        return filter_query_set

    def check_creator_when_delete(self, instance):
        # domain_id = self.request.data.get("jwt").domain_id

        domain_id = self.request.jwt.domain_id
        is_admin = self.request.jwt.system_admin
        if not str(domain_id) in instance.creator and not is_admin:
            raise Exception(
                "user: <{}> is not creator or admin, can't delete data".format(domain_id))

    def auth_user_when_update_creator_owner(self, instance, validated_data):
        if instance.creator != validated_data.get("creator") or instance.owner != validated_data.get("owner"):
            # domain_id = self.context.get("request").data.get("jwt").domain_id
            # is_admin = self.context.get("request").data.get("jwt").system_admin
            domain_id = self.context.get("request").jwt.domain_id
            is_admin = self.context.get("request").jwt.system_admin
            if not str(domain_id) in instance.creator and not is_admin:
                raise Exception(
                    "user: <{}> is not creator or admin, can't update_creator_owner data".format(domain_id))


##########################group mixin###########################
class OperateCreatorRetrieveModelMixin(OperateCreatorOwnerFieldMixin, DefaultRetrieveModelMixin):
    pass


class OperateCreatorListModelMixin(OperateCreatorOwnerFieldMixin, DefaultListModelMixin):
    pass


class TaskCreateModelMixin(DefaultCreateModelMixin, TaskModelMixin):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return DefaultResponse(code=False, msg=str(serializer.errors))
        try:
            with transaction.atomic():
                self.perform_create(serializer)
                self.create_task(serializer)
        except Exception as e:
            return DefaultResponse(code=False, msg=str(e))
        headers = self.get_success_headers(serializer.data)
        return DefaultResponse(serializer.data, headers=headers)


class TaskDestroyModelMixin:

    def perform_destroy(self, instance):
        # check ref
        # if instance.referenced:
        #     raise Exception("删除失败，资源id: {}的referenced: {}被引用".format(
        #         instance.id, instance.referenced))
        # handle task
        self.bulk_del_task("delete task")

        instance.delete()

    def perform_destroy_many(self, ids):
        queryset = self.get_queryset()
        querysets = queryset.filter(pk__in=ids)
        if len(list(querysets)) <= 0:
            raise Exception("批量删除失败, 查询数据为：{}".format(list(querysets)))

        # handle task
        # self.bulk_del_task("delete task")

        # for instance in list(querysets):  # for remote ref restrict
        #     if instance.referenced:
        #         # print(instance.referenced)
        #         raise Exception("批量删除失败，资源id: {}的referenced: {}被引用".format(
        #             instance.id, instance.referenced))

        querysets.delete()


class AddPKUpdateModelMixin(DefaultUpdateModelMixin):

    def update(self, request, *args, **kwargs):
        # print(request)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        # validate_logic_phy_ap_unique via pk
        serializer.pk = kwargs.get("pk")
        if not serializer.is_valid():
            return DefaultResponse(code=False, msg=str(serializer.errors))
        try:
            self.perform_update(serializer)
        except Exception as e:
            return DefaultResponse(code=False, msg=str(e))

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return DefaultResponse(serializer.data)


class TaskUpdateModelMixin(DefaultUpdateModelMixin):
    """
    update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return DefaultResponse(code=False, msg=str(serializer.errors))
        try:
            with transaction.atomic():
                self.perform_update(serializer)
                # self.update_task(request)
        except Exception as e:
            return DefaultResponse(code=False, msg=str(e))

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return DefaultResponse(serializer.data)

    def update_task(self, serializer):
        contract_remind = serializer.data.get("contract_remind")
        if not contract_remind:
            return
        # del old task by contractid
        # create new task by contractid
        # use contract id as task name
        # start sheduler

        end_date = serializer.data.get("end_date")
        timer = datetime.datetime.strptime(
            end_date, '%Y-%m-%d').date() + datetime.timedelta(days=-contract_remind)
        # print(timer)
        # if create task fail raise exception
        # if not serializer:
        #     raise Exception("no found")
        # print("updated task by contractid: {}".format(serializer.data.get("id")))


class CheckRefDestroyModelMixin():
    """
    Destroy a model instance with check ref action
    """

    def perform_destroy(self, instance):
        if instance.referenced:
            raise Exception("删除失败，资源id: {}的referenced: {}被引用".format(
                instance.id, instance.referenced))
            # return DefaultResponse(msg="删除失败，资源id: {}的referenced: {}被引用".format(instance.id, instance.referenced), code=False, status=status.HTTP_200_OK)
        instance.delete()

    def perform_destroy_many(self, ids):
        queryset = self.get_queryset()
        querysets = queryset.filter(pk__in=ids)
        if len(list(querysets)) <= 0:
            raise Exception("批量删除失败, 查询数据为：{}".format(list(querysets)))
            # return DefaultResponse(status=status.HTTP_200_OK, code=False, msg="批量删除失败, 查询数据为：{}".format(list(querysets)))
        for instance in list(querysets):  # for remote ref restrict
            if instance.referenced:
                # print(instance.referenced)
                raise Exception("批量删除失败，资源id: {}的referenced: {}被引用".format(
                    instance.id, instance.referenced))
        querysets.delete()


class RefUpdateModelMixin:
    """ update ref field mixin """
    @action(methods=['PATCH'], detail=False)
    def update_reference(self, request):
        """
        data structure:
        {
            "objs": [
                {
                    "ids": [
                        1,
                        2
                    ],
                    "action": "del_ref",
                    "referenced": {
                        "test": "test",
                        "test2": "test2"
                    }
                }
            ]
        }
        """
        serializer = BulkOperateReferenceSerializer2(
            meta_class=self.model_class, data=request.data)
        try:
            if not serializer.is_valid():
                # not return code=False when ids not found
                # print(serializer.errors)
                return DefaultResponse(code=False, msg=str(serializer.errors))
        except Exception as e:
            # print(str(e))
            return DefaultResponse(code=False, msg=str(e))

        try:
            self.perform_update(serializer)
        except Exception as e:
            # print(str(e))
            return DefaultResponse(code=False, msg=str(e))
        return DefaultResponse(status=status.HTTP_200_OK)

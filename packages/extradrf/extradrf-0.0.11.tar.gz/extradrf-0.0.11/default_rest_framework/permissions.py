from rest_framework import permissions
from rest_framework.authentication import get_authorization_header
from utils import JWTModel


class AuthPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        request.user is token user
        Return `True` if permission is granted, `False` otherwise.
        """
        # print('view.action: ', view.action)
        # print('view.basename: ', view.basename)
        # print('get_view_name: ', view.get_view_name())
        # print('get_view_description: ', view.get_view_description())
        # print('request.user: ', request.user)
        # print(dir(view))
        # print(dir(request.user))
        # print(request.user.id)
        # print("----------------")
        # print('request.user.get_all_permissions: ',
        #       request.user.get_all_permissions())
        # print("----------------")
        # print('request.user.get_group_permissions: ',
        #       request.user.get_group_permissions())
        # print("----------------")
        # print('request.user.user_permissions: ', request.user.user_permissions)
        # if request.META.get("HTTP_TEST"):
        #     return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        GET http://10.2.2.5:8001/user/2/
        Return `True` if permission is granted, `False` otherwise.
        """
        # print('view.action: ', view.action)
        # print('request.user: ', request.user)
        # print('obj: ', obj)
        # authenticator = self.get_authenticators()[0]
        # user, _ = authenticator.authenticate(request)
        # print(obj)
        if request.META.get("HTTP_AUTHORIZATION") and obj.id == 2:
            return True
        return False


class CustomJWTPermission(permissions.BasePermission):
    """  """

    def has_permission(self, request, view):
        try:
            message = get_authorization_header(request).split()[1]
        except IndexError:
            return False
        jwt = JWTModel(message.decode())

        # self.jwt = jwt
        request.jwt = jwt
        return jwt.has_permission(request.path, request.method)

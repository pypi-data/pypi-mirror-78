from rest_framework import views
from rest_framework import exceptions
from rest_framework import status
from .response import DefaultResponse

class DefaultAPIView(views.APIView):
    """  """

    def handle_exception(self, exc):
        """
        customize Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        super().handle_exception(exc)
        # if isinstance(exc, (exceptions.NotAuthenticated,
        #                     exceptions.AuthenticationFailed)):
        #     # WWW-Authenticate header for 401 responses, else coerce to 403
        #     auth_header = self.get_authenticate_header(self.request)

        #     if auth_header:
        #         exc.auth_header = auth_header
        #     else:
        #         exc.status_code = status.HTTP_403_FORBIDDEN

        # exception_handler = self.get_exception_handler()

        # context = self.get_exception_handler_context()
        # response = exception_handler(exc, context)

        # if response is None:
        #     self.raise_uncaught_exception(exc)

        # response.exception = True
        # return response
        return DefaultResponse(
                code=False,
                msg=exc.default_detail, 
                # data=str(exc.default_detail), 
                # status=exc.status_code
            )
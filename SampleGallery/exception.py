from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if len(exc.args)>0 and isinstance(exc.args[0], ReturnDict) :
        response.data['detail'] = list(exc.args[0].values())[0][0]

    return response

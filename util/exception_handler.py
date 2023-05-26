from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if response.data and isinstance(response.data, dict):
            response.data["success"] = False

            if "detail" in response.data:
                response.data["message"] = response.data.get("detail")

            if "message" not in response.data and response.status_code == status.HTTP_400_BAD_REQUEST:
                response.data["message"] = "Something went wrong, please try again"

        if "non_field_errors" in response.data:
            errors = response.data.pop("non_field_errors")
            response.data["message"] = ", ".join([str(e) for e in errors])

    return response

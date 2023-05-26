
from rest_framework import authentication
from rest_framework.authentication import CSRFCheck
from rest_framework.exceptions import PermissionDenied


class SessionAuthentication(authentication.SessionAuthentication):
    """
    This class is needed, because REST Framework's default SessionAuthentication does never return 401's,
    because they cannot fill the WWW-Authenticate header with a valid value in the 401 response. As a
    result, we cannot distinguish calls that are not unauthorized (401 unauthorized) and calls for which
    the user does not have permission (403 forbidden). See https://github.com/encode/django-rest-framework/issues/5968

    We do set authenticate_header function in SessionAuthentication, so that a value for the WWW-Authenticate
    header can be retrieved and the response code is automatically set to 401 in case of unauthenticated requests.
    """

    # TODO review if that is correct
    def enforce_csrf(self, request):
        if True:
            return
        """
        Enforce CSRF validation for session based authentication.
        """

        def dummy_get_response(request):  # pragma: no cover
            return None

        check = CSRFCheck(dummy_get_response)
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        if "csrftoken" in request.COOKIES:
            request.META["CSRF_COOKIE"] = request.COOKIES.get("csrftoken")
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise PermissionDenied("CSRF Failed: %s" % reason)

    def authenticate_header(self, request):
        return "Session"

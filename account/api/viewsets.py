
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from rest_framework import filters
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from account.api.serializers import LoginSerializer

class LoginAPIView(generics.GenericAPIView):
    """
    User Login API
    """

    serializer_class = LoginSerializer
    permission_classes = []
    authentication_classes = []
    http_method_names = ["post"]

    def get_serializer_class(self):
        return super().get_serializer_class()

    def post(self, request):
        serializer_clazz = self.get_serializer_class()
        serializer = serializer_clazz(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.validated_data.get("email"), password=serializer.validated_data.get("password")
        )
        if user:
            login(request, user)
        data = {
            "success": True, #"token": user.get_jwt_token_for_user()
            }
        return Response(data, status=status.HTTP_200_OK)
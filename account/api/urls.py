
from django.urls import path

from account.api.viewsets import (
    LoginAPIView,
)

urlpatterns = [
    path("account/auth/login/", LoginAPIView.as_view(), name="login-api"),
   
]

from django.conf import settings
from django.contrib import auth
from django.core.cache import cache
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from account.models import User, USER_TYPE_ADMIN




class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for login view
    """

    email = serializers.EmailField(max_length=255, min_length=8, help_text="User email address")
    password = serializers.CharField(
        style={"input_type": "password"},
        max_length=50,
        min_length=3,
        write_only=True,
        help_text="User password",
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = User.objects.filter(email=email).first()
        if user:
            if not user.is_active:
                raise ValidationError("This account is currently disabled")
            user_auth = auth.authenticate(email=email, password=password)
            if not user_auth:
                response = {"success": False, "message": "Invalid email or password"}
                raise AuthenticationFailed(response)
            user_auth.last_login = timezone.now()
            user_auth.save()
        else:
            raise ValidationError("Invalid email or password")

        return super().validate(attrs)

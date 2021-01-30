from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """

    password = serializers.CharField(min_length=5, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "created_at",
            "updated_at",
            "password",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "bio": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username")

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should only contain alphanumeric characters."
            )

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for email verification with token
    """

    token = serializers.CharField()


class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login
    """

    class Meta:
        model = User
        fields = ("email", "password", "username", "tokens")

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    username = serializers.CharField(read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])

        return {
            "access": user.tokens.get("access"),
            "refresh": user.tokens.get("refresh"),
        }

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        tokens = attrs.get("tokens")

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("invalid credentials, try again.")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin.")
        if not user.is_verified:
            raise AuthenticationFailed("Account is not verified.")

        return {
            "email": user.email,
            "username": user.username,
            "tokens": tokens,
        }


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout
    """

    refresh = serializers.CharField()
    default_error_messages = {"bad_token": "Token is expired or invalid."}

    def validate(self, attrs):
        self.token = attrs.get("refresh", "")
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()

        except TokenError:
            self.fail("bad_tokens")

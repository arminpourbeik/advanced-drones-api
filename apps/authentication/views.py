import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from decouple import config

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.sites.shortcuts import get_current_site

from apps.authentication.models import User
from .serializers import (
    RegistrationSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
)
from .utils import Util
from .renderers import UserRenderer


class RegisterApiView(generics.GenericAPIView):
    """
    View for user registration
    """

    serializer_class = RegistrationSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])

        token = RefreshToken.for_user(user=user).access_token

        current_site = get_current_site(request=request).domain
        relative_link = reverse("email_verify")
        absolute_url = f"http://{current_site}{relative_link}?token={str(token)}"

        email_body = f"{user.username}, use the link below to verify your email \n {absolute_url}"
        data = {
            "body": email_body,
            "to": user.email,
            "subject": "verify your email",
        }

        Util.send_email(data)

        return Response({"msg": user_data}, status=status.HTTP_201_CREATED)


class VerifyEmailApiView(generics.GenericAPIView):
    """
    View for email verification
    """

    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get("token")

        try:
            payload = jwt.decode(token, config("DJANGO_SECRET_KEY"), algorithms="HS256")
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {"msg": "Successfully activated"}, status=status.HTTP_200_OK
            )

        except ExpiredSignatureError:
            return Response(
                {"error": "Activation link expired"}, status=status.HTTP_400_BAD_REQUEST
            )

        except DecodeError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginApiView(generics.GenericAPIView):
    """
    View for user login
    """

    serializer_class = LoginSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutApiView(generics.GenericAPIView):
    """
    View for user logout
    """

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("register/", views.RegisterApiView.as_view(), name="register"),
    path("verify-email/", views.VerifyEmailApiView.as_view(), name="email_verify"),
    path("login/", views.LoginApiView.as_view(), name="login"),
    path("logout/", views.LogoutApiView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

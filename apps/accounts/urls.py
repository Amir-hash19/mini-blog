from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView, TokenVerifyView

from .views import UserRegistrationView, UserLoginView, UserProfileView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path("register/", UserRegistrationView.as_view(), name="resgister-user"),
    path("login/", UserLoginView.as_view(), name="login-user"),

    path("profile/", UserProfileView.as_view(), name="user-profile"),
]
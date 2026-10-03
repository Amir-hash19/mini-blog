from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView, TokenVerifyView

from rest_framework.routers import DefaultRouter

from .views import UserRegistrationView, UserLoginView, UserProfileView, ProfileUpdateViewSet


router = DefaultRouter()

router.register(
    r"profile/update",
    ProfileUpdateViewSet,
    basename="profile-update"
)

urlpatterns = [
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path(
        "token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),

    path(
        "register/",
        UserRegistrationView.as_view(),
        name="register-user",
    ),

    path(
        "login/",
        UserLoginView.as_view(),
        name="login-user",
    ),

    path(
        "profile/",
        UserProfileView.as_view(),
        name="user-profile",
    ),
]

urlpatterns += router.urls
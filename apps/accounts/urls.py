from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView, TokenVerifyView

from .views import UserRegistrationView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path("register/", UserRegistrationView.as_view(), name="resgister-user"),
]
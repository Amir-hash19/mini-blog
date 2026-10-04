from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CreatePostView

urlpatterns = [
    path(
        "create/",
        CreatePostView.as_view(),
        name="create-post"
    )
]
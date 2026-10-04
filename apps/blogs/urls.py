from django.urls import path
from .views import CreatePostView, PostDeleteDetailView, PostUpdateView

urlpatterns = [
    path(
        "create/",
        CreatePostView.as_view(),
        name="create-post"
    ),

    path(
        "<int:post_id>/",
        PostDeleteDetailView.as_view(),
        name="post-detail"
    ),

    path(
        "<int:post_id>/edit/",
        PostUpdateView.as_view(),
        name="post-update"
    )
]
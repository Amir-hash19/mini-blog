from django.urls import path

from .views import (
    CommentCreateView,
    CommentDetailView,
    CreateLikeView,
    CreatePostView,
    PostDeleteDetailView,
    PostListView,
    PostUpdateView,
)

urlpatterns = [
    path("create/", CreatePostView.as_view(), name="create-post"),
    path("<int:post_id>/", PostDeleteDetailView.as_view(), name="post-detail"),
    path("<int:post_id>/edit/", PostUpdateView.as_view(), name="post-update"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("comments/", CommentCreateView.as_view(), name="comment-list-create"),
    path(
        "<int:post_id>/comments/<int:comment_id>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
    path("likes/", CreateLikeView.as_view(), name="like-create"),
]

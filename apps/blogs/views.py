import logging

from django.db import transaction
from rest_framework import generics, mixins, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Like, Post
from .permissions import IsCommentAuthorOrReadOnly

logger = logging.getLogger(__name__)

from .serializers import CommentSerializer, LikeSerializer, PostSerializer


class CreatePostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDeleteDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"
    lookup_url_kwarg = "post_id"


class PostUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"
    lookup_url_kwarg = "post_id"


class PostListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_fields = ["status", "author__username"]
    search_fields = ["content", "author__username"]
    ordering_fields = ["created_at", "updated_at", "published_at", "views_count"]
    ordering = ["-created_at"]  # Default ordering


class CreateComment(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.select_related("author", "post", "parent").all()

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsCommentAuthorOrReadOnly,
    ]
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"


class CreateLikeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

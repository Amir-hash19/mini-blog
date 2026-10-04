from rest_framework import status, mixins, generics
from rest_framework.response import Response
import logging
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post
from django.db import transaction

logger = logging.getLogger(__name__)

from .serializers import PostSerializer


class CreatePostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
   




class PostDeleteDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'





class PostUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"
    lookup_url_kwarg = "post_id"
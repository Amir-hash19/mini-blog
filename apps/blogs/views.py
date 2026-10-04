from rest_framework import status, mixins, generics
from rest_framework.response import Response
import logging
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post, Comment, Like
from django.db import transaction

logger = logging.getLogger(__name__)

from .serializers import PostSerializer


class CreatePostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
   
 
from rest_framework import serializers
from .models import Post

from django.utils import timezone


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    class Meta:
        model = Post
        fields = [
            'content','cover_image', 
            'status', 'author',
            'views_count', 'created_at', 
            'updated_at', 'published_at'
                ]
        read_only_fields = ['author', 'views_count', 'created_at', 'updated_at', 'published_at']

    def create(self, validated_data):
        author = self.context["request"].user

        if validated_data.get("status") == Post.Status.PUBLISHED:
            validated_data["published_at"] = timezone.now()

        return Post.objects.create(
            author=author,
            **validated_data
        )
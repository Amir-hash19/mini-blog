from django.utils import timezone
from rest_framework import serializers

from apps.activities.events import ActivityEvent
from apps.activities.publisher import publish_event

from .models import Comment, Like, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = [
            "content",
            "cover_image",
            "status",
            "author",
            "views_count",
            "created_at",
            "updated_at",
            "published_at",
        ]
        read_only_fields = [
            "author",
            "views_count",
            "created_at",
            "updated_at",
            "published_at",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        author = self.context["request"].user

        if validated_data.get("status") == Post.Status.PUBLISHED:
            validated_data["published_at"] = timezone.now()

        post = Post.objects.create(author=author, **validated_data)

        publish_event(
            ActivityEvent(
                user_id=author.id,
                action="post_created",
                target_type="post",
                target_id=post.id,
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
                metadata={
                    "status": post.status,
                },
            )
        )

        return post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), write_only=True
    )

    class Meta:
        model = Comment
        fields = ["post", "author", "content", "parent", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):

        return Comment.objects.create(
            author=self.context["request"].user, **validated_data
        )


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), write_only=True
    )

    class Meta:
        model = Like
        fields = ["post", "user", "created_at"]
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        return Like.objects.create(user=self.context["request"].user, **validated_data)

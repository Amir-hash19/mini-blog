from rest_framework import serializers

from apps.activities.events import ActivityEvent
from apps.activities.publisher import publish_event


from .models import Profile, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def create(self, validated_data):
        request = self.context.get("request")
        if validated_data["password"] != validated_data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        publish_event(
            ActivityEvent(
                user_id=user.id,
                action="user_registered",
                target_type="user",
                target_id=user.id,
                ip_address=request.META.get("REMOTE_ADDR") if request else None,
                user_agent=request.META.get("HTTP_USER_AGENT") if request else None,
                metadata={
                    "username": user.username,
                }
            )
        )

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        request = self.context.get("request")
        username = data.get("username")
        password = data.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid username or password.")
        
        publish_event(
            ActivityEvent(
                user_id=user.id,
                action="user_login",
                target_type="user",
                target_id=user.id,
                ip_address=request.META.get("REMOTE_ADDR") if request else None,
                user_agent=request.META.get("HTTP_USER_AGENT") if request else None,
            )
        )
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["bio", "avatar", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            "avatar",
            "bio",
        ]

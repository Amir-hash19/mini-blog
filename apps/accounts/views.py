import logging

from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from apps.activities.events import ActivityEvent
from apps.activities.publisher import publish_event


from .models import Profile, User
from .serializers import (
    ProfileSerializer,
    ProfileUpdateSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


class UserRegistrationView(APIView):
    """
    API view for user registration.
    """

    permision_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):

        logger.info(f"User registration request data: {request.data}")

        serializer = UserRegistrationSerializer(
            data=request.data,
            context={"request": request}
        
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        logger.info(f"User registered successfully: {user.username}")

        refresh = RefreshToken.for_user(user)

        logger.info(f"JWT tokens generated for user: {user.id}")

        return Response(
            {
                "user": UserRegistrationSerializer(user).data,
                "message": "User registered successfully.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    """
    API view for user login.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        user = User.objects.get(username=username)

        refresh = RefreshToken.for_user(user)

        logger.info(f"User logged in successfully:{user.id}")

        return Response(
            {
                "user": UserLoginSerializer(user).data,
                "message": " User Logged in successfully.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class UserProfileView(RetrieveAPIView):
    """
    API view for retrieving user profile.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.select_related("profile").get(id=self.request.user.id)


class ProfileUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    API view for updating user profile.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUpdateSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.request.user.profile


class UserLogOut(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        user = request.user
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"detail":"Refresh token required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            publish_event(
                ActivityEvent(
                    user_id=user.id,
                    action="user_logout",
                    target_type="user",
                    target_id=user.id,
                    ip_address=request.META.get("REMOTE_ADDR") if request else None,
                    user_agent=request.META.get("HTTP_USER_AGENT") if request else None,
                    
                )
            )

            return Response(
                {"message":"User Logout was Successful."},
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {
                    "detail":"Invalid Token"
                }, status=status.HTTP_400_BAD_REQUEST
            )
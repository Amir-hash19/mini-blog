from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.db import transaction

import logging
from .models import User

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, ProfileSerializer


logger = logging.getLogger(__name__)


class UserRegistrationView(APIView):
    """
    API view for user registration.
    """
    permision_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):

        logger.info(f"User registration request data: {request.data}")

        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        logger.info(f"User registered successfully: {user.username}")

        refresh = RefreshToken.for_user(user)

        logger.info(f"JWT tokens generated for user: {user.id}")

        return Response({
            "user":UserRegistrationSerializer(user).data,
            'message': 'User registered successfully.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)




class UserLoginView(APIView):
    """
    API view for user login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
       
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        

        username = serializer.validated_data['username']
        user = User.objects.get(username=username)

        refresh = RefreshToken.for_user(user)

        logger.info(f"User logged in successfully:{user.id}")

        return Response({
            "user": UserLoginSerializer(user).data,
            "message":" User Logged in successfully.",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)



class UserProfileView(RetrieveAPIView):
    """
    API view for retrieving user profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return (
            User.objects.select_related("profile")
            .get(id=self.request.user.id)
        )

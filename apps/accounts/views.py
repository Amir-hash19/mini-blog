from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

import logging


from .serializers import UserRegistrationSerializer


logger = logging.getLogger(__name__)


class UserRegistrationView(APIView):
    """
    API view for user registration.
    """
    permision_classes = [AllowAny]
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

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User, UserProfile
from authentication.serializers import UserSerializer, UserProfileSerializer



# Authentication views for user registration, login, logout, and token management
class SignUpView(generics.GenericAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "User created successfully",
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                    }
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


login_view = TokenObtainPairView.as_view()

refresh_token_view = TokenRefreshView.as_view()


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAdminUser,]
    serializer_class = UserSerializer
    queryset = User.objects.all()     



# User profile view to retrieve and update user profile information
class UserProfileAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserProfileSerializer

    def get_object(self, user):
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return UserProfile.objects.create(user=user)

    def get(self, request):
        user_profile = self.get_object(user=request.user)
        serializer = self.serializer_class(user_profile)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user_profile = self.get_object(user=request.user)
        serializer = self.serializer_class(instance=user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        user_profile = self.get_object(user=request.user)
        serializer = self.serializer_class(instance=user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

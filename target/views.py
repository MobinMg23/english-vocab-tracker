from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from target.permissions import IsOwner

from target.models import LearningTarget
from target.serializers import LearningTargetSerializer

    

class LearningTargetAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LearningTargetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LearningTargetListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LearningTargetSerializer

    def get_queryset(self):
        return LearningTarget.objects.filter(user=self.request.user)
    

class LearningTargetDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LearningTargetSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return LearningTarget.objects.filter(user=self.request.user)

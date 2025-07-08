from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from target.permissions import IsOwner

from target.models import LearningTarget, DailyMission
from target.serializers import LearningTargetSerializer, DailyMissionSerializer

    

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
    

class LearningTargetDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner,]
    serializer_class = LearningTargetSerializer
    
    def get(self, request, pk):
        target = get_object_or_404(LearningTarget, pk=pk, user=request.user)
        serializer = self.serializer_class(target)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        target = get_object_or_404(LearningTarget, pk=pk, user=request.user)
        serializer = self.serializer_class(instance=target, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        target = get_object_or_404(LearningTarget, pk=pk, user=request.user)
        target.delete()
        
        return Response({"message": "Learning target deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

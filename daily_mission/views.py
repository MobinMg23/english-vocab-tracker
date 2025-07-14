from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from target.permissions import IsOwner
from daily_mission.models import DailyMission
from daily_mission.serializers import DailyMissionSerializer
from target.models import LearningTarget
from celery_tasks.daily_mission_tasks.create_daily_mission_task import create_daily_mission


class CreateDailyMission(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = DailyMissionSerializer

    def get(self, request):
        create_daily_mission.apply_async(args=[request.user.id], countdown=3)
        return Response({})



class DailyMissionTodayAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = DailyMissionSerializer

    def get_queryset(self):
        return DailyMission.objects.filter(
            target__user=self.request.user,
            datetime__date=timezone.now().date()
        )


class DailyMissionListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = DailyMissionSerializer

    def get_queryset(self):
        return DailyMission.objects.filter(target__user=self.request.user)
    

class DailyMissionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = DailyMissionSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return DailyMission.objects.filter(target__user=self.request.user)
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from target.permissions import IsOwner

from daily_mission.models import DailyMission
from daily_mission.serializers import DailyMissionSerializer
from target.models import LearningTarget
from target.serializers import LearningTargetSerializer



class CreateDailyMissionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = DailyMissionSerializer

    def get(self, request):
        pass


class DailyMissionListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner,]
    serializer_class = DailyMissionSerializer

    def get_queryset(self):
        return DailyMission.objects.filter(target__user=self.request.user).order_by('-datetime')
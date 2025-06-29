from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from target.permissions import IsOwner
from word.models import Word
from word.serializers import WordSerializer

from celery_tasks.word_tasks.word_save_task import word_save_task



class WordSaveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        file = request.FILES.get('file')
        category = request.data.get('category', 'short')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        content = file.read().decode('utf-8')
        words = content.splitlines()
        if not words:
            return Response({"error": "File is empty"}, status=status.HTTP_400_BAD_REQUEST)

        delay = 0
        for word in words:
            word_save_task.apply_async(args=[category, word], countdown=delay)
            delay += 5

        return Response({"message": "Words saved successfully"}, status=status.HTTP_201_CREATED)
    

class WordListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = WordSerializer

    def get_queryset(self):
        return Word.objects.all()  


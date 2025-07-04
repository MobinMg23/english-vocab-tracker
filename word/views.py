from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from target.permissions import IsOwner
from word.models import Word, Translation, LearnedWord
from word.serializers import WordSerializer, TranslationSerializer

from celery_tasks.word_tasks.word_save_task import word_save_task
from celery_tasks.word_tasks.word_translate_task import word_translate_task



class WordSaveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser,]

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
    permission_classes = [AllowAny,]
    serializer_class = WordSerializer

    def get_queryset(self):
        return Word.objects.all()  


class WordDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = WordSerializer

    def get_object(self, word):
        try:
            return Word.objects.get(name=word)
        except Word.DoesNotExist:
            raise Http404

    def get(self, request, word):
        word = self.get_object(word=word)
        serializer = self.serializer_class(word)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class WordTranslateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self, language=None):
        words = Word.objects.all()
        not_translated_words = [word for word in words if not Translation.objects.filter(word=word, language=language).exists()]
        return not_translated_words
    
    def post(self, request, language):
        words = self.get_queryset(language=language)
        if not words:
            return Response({"message": "No words to translate"}, status=status.HTTP_404_NOT_FOUND)
        
        for word in words:
            word_translate_task.apply_async(args=[word.id, language], countdown=5)  

        return Response({"message": "Translation task started"}, status=status.HTTP_202_ACCEPTED)


class WordTranslateDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TranslationSerializer

    def get_object(self, word, language):
        return Translation.objects.filter(word=word, language=language).first()

    def get(self, request, word, language):
        word = get_object_or_404(Word, name=word)
        translation = self.get_object(word, language)       
        if not translation:
            return Response({"error": "Translation not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(translation)

        return Response(serializer.data, status=status.HTTP_200_OK)
        

    

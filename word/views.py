from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from target.permissions import IsOwner
from word.models import Word, Translation, LearnedWord
from word.serializers import WordSerializer, TranslationSerializer, LearnedWordSerializer

from celery_tasks.word_tasks.word_save_task import word_save_task
from celery_tasks.word_tasks.word_translate_task import word_translate_task


class WordSaveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        file = request.FILES.get('file')
        category = request.data.get('category', 'SHORT').upper()

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        content = file.read().decode('utf-8')
        words = set(filter(None, content.splitlines()))
        if not words:
            return Response({"error": "File is empty"}, status=status.HTTP_400_BAD_REQUEST)

        for i, word in enumerate(words):
            word_save_task.apply_async(args=[category, word], countdown=i * 5)

        return Response({"message": "Words saved successfully"}, status=status.HTTP_201_CREATED)
    

class WordListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = WordSerializer
    queryset = Word.objects.all()


class WordDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = WordSerializer

    def get(self, request, word):
        word = get_object_or_404(Word, name=word)
        serializer = self.serializer_class(word)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class WordTranslateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        language = self.kwargs.get('language')
        return Word.objects.exclude(translation__language=language)

    def post(self, request, language):
        words = self.get_queryset()
        if not words.exists():
            return Response({"message": "No words to translate"}, status=status.HTTP_404_NOT_FOUND)

        for i, word in enumerate(words):
            word_translate_task.apply_async(args=[word.id, language], countdown=i * 5)

        return Response({"message": "Translation task started"}, status=status.HTTP_202_ACCEPTED)


class WordTranslateDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TranslationSerializer

    def get(self, request, word, language):
        translation = get_object_or_404(Translation, word__name=word, language=language)       
        serializer = self.serializer_class(translation)

        return Response(serializer.data, status=status.HTTP_200_OK)
        

class LearnedWordListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LearnedWordSerializer   

    def get_queryset(self):
        return LearnedWord.objects.filter(user=self.request.user).select_related('word')
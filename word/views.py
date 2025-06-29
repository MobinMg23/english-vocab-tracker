from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from target.permissions import IsOwner



class WordSaveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        file = request.FILES.get('*.txt')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        content = file.read().decode('utf-8')
        words = content.splitlines()
        if not words:
            return Response({"error": "File is empty"}, status=status.HTTP_400_BAD_REQUEST)

        for word in words:
            
            
            pass  

        return Response({"message": "Words saved successfully"}, status=status.HTTP_201_CREATED)

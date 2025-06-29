from django.urls import path
from word.views import WordSaveAPIView, WordListAPIView


urlpatterns = [
    path('save/', WordSaveAPIView.as_view(), name='word-save'),
    path('list/', WordListAPIView.as_view(), name='word-list'),
]

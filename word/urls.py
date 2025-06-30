from django.urls import path
from word.views import (WordSaveAPIView, WordListAPIView, WordDetailAPIView,
                         WordTranslateAPIView, WordTranslateDetailAPIView)


urlpatterns = [
    path('save/', WordSaveAPIView.as_view(), name='word-save'),
    path('list/', WordListAPIView.as_view(), name='word-list'),
    path('detail/<str:word>/', WordDetailAPIView.as_view(), name='word-detail'),
    path('translate/<str:language>/all/', WordTranslateAPIView.as_view(), name='word-translate'),
    path('translate/<str:language>/detail/<str:word>/', WordTranslateDetailAPIView.as_view(), name='word-translate-detail'),

]

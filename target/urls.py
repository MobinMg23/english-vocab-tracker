from django.urls import path
from target.views import LearningTargetAPIView, LearningTargetListAPIView, LearningTargetDetailAPIView

urlpatterns = [
    path('create/', LearningTargetAPIView.as_view(), name='target-create'),
    path('list/', LearningTargetListAPIView.as_view(), name='target-list'),
    path('detail/<int:id>/', LearningTargetDetailAPIView.as_view(), name='target-detail'),
]
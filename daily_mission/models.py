from django.db import models
from django.utils import timezone
from word.models import Word
from target.models import LearningTarget


class DailyMissionManager(models.Manager):
    def get_today_mission(self, user):
        today = timezone.now().date()
        return self.filter(target__user=user, datetime__date=today).order_by('-datetime')
    
class DailyMission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    title = models.CharField(max_length=20, blank=True, null=True)
    target = models.ForeignKey(LearningTarget, on_delete=models.CASCADE, related_name='daily_mission_targets')
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=10)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.target.title} ({self.status})"
        

class DailyMissionWord(models.Model):
    daily_mission = models.ForeignKey(DailyMission, on_delete=models.CASCADE, related_name='daily_words')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.daily_mission.title} - {self.word.name}"
    
    class Meta:
        unique_together = ('daily_mission', 'word')
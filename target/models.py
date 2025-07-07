from django.db import models
from django.utils import timezone
from datetime import timedelta
from authentication.models import User
#from word.models import Word


def default_end_date():
    return timezone.now().date() + timedelta(days=30)

class LearningTarget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    daily_goal = models.PositiveIntegerField(default=1)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=default_end_date)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    


    




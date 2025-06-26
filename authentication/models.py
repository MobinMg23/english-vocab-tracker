from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    words_count_learned = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"



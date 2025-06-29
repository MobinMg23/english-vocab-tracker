from django.db import models
from django.utils import timezone
from authentication.models import User
from target.models import LearningTarget


class Word(models.Model):
    CATEGORY_CHOICES = [
        ('SHORT', 'short'),
        ('MEDIUM', 'short'),
        ('LONG', 'long'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, default='SHORT')
    definition = models.TextField()
    example = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class TranslationManager(models.Manager):
    
    def get_word_translation(self, word, language):
        return self.filter(word=word, language=language).values_list('translation', flat=True)
    
    def get_example_translation(self, word, language):
        return self.filter(word=word, language=language).values_list('example', flat=True).first()

class Translation(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    word_translation = models.CharField(max_length=200)
    LANG_CHOICES = [
    ('en', 'English'),
    ('fa', 'Persian'),
    ('es', 'Spanish'),
    ]
    example_translation = models.TextField(blank=True, null=True)
    language = models.CharField(choices=LANG_CHOICES, default='fa', max_length=20)
    objects = TranslationManager()

    def __str__(self):
        return f"{self.word_translation.name} ({self.language}): {self.word_translation}"
    
    class Meta:
        unique_together = ('word', 'language')


class LearnedWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(LearningTarget, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    learned_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.word.word} - {self.user.username}"
    
    class Meta:
        unique_together = ('user', 'word')

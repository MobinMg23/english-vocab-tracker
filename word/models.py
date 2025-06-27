from django.db import models
from django.utils import timezone
from authentication.models import User
from target.models import LearningTarget



class WordCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    

class Word(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(WordCategory, on_delete=models.CASCADE)
    definition = models.TextField()
    example = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class WordTranslationManager(models.Manager):

    def get_translations(self, word, language):
        return self.filter(word=word, language=language).values_list('translation', flat=True)

class WordTranslation(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    LANG_CHOICES = [
    ('en', 'English'),
    ('fa', 'Persian'),
    ('es', 'Spanish'),
    ]
    language = models.CharField(choices=LANG_CHOICES, default='fa', max_length=20)
    translation = models.CharField(max_length=200)
    objects = WordTranslationManager()

    def __str__(self):
        return f"{self.word.name} ({self.language}): {self.translation}"
    
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




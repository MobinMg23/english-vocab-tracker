from rest_framework import serializers
from word.models import Word, Translation, LearnedWord


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'name', 'category', 'definition', 'example']
        read_only_fields = ['id']


class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['id', 'word', 'word_translation', 'example_translation', 'language']
        read_only_fields = ['id', 'word'] 


class LearnedWordSerializer(serializers.ModelSerializer):
    word_name = serializers.CharField(source='word.name')
    class Meta:
        model = LearnedWord
        fields = ['id', 'user', 'word','target','word_name', 'learned_date']
        read_only_fields = ['id', 'user', 'word']

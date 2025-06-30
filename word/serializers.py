from rest_framework import serializers
from word.models import Word, Translation


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
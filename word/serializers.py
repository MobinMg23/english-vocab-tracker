from rest_framework import serializers
from word.models import Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'name', 'category', 'definition', 'example']
        read_only_fields = ['id']
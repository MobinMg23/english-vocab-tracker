from rest_framework import serializers
from target.models import LearningTarget


class LearningTargetSerializer(serializers.ModelSerializer):

    class Meta:
        model = LearningTarget
        fields = ['title', 'description', 'daily_goal', 'start_date', 'end_date']
        
    def create(self, validated_data):
        user = self.context['request'].user
       
        return LearningTarget.objects.create(user=user, **validated_data)
        

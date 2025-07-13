from rest_framework import serializers
from daily_mission.models import DailyMission


class DailyMissionSerializer(serializers.ModelSerializer):
    daily_words_goal = serializers.SerializerMethodField()
    words = serializers.SerializerMethodField()

    class Meta:
        model = DailyMission
        fields = ['title', 'target', 'status', 'datetime', 'words', 'daily_words_goal']

    def get_daily_words_goal(self, obj):
        
        return obj.target.daily_goal

    def get_words(self, obj):
        
        return obj.daily_words.all()
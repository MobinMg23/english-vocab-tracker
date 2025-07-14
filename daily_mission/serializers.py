from rest_framework import serializers
from daily_mission.models import DailyMission, DailyMissionWord
from word.models import Word
from word.serializers import WordSerializer



class DailyMissionWordSerializer(serializers.ModelSerializer):
    word = WordSerializer()

    class Meta:
        model = DailyMissionWord
        fields = ['word']


class DailyMissionSerializer(serializers.ModelSerializer):
    daily_words_goal = serializers.SerializerMethodField()
    words = DailyMissionWordSerializer(source='daily_words', many=True)

    class Meta:
        model = DailyMission
        fields = ['title', 'target', 'status', 'datetime', 'words', 'daily_words_goal']

    def get_daily_words_goal(self, obj):
        return obj.target.daily_goal

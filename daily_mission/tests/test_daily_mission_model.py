from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from daily_mission.models import DailyMission, DailyMissionWord
from target.models import LearningTarget
from word.models import Word


User = get_user_model()



class DailyMissionTests(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='mobin', password='Aa1100')

        self.target1 = LearningTarget.objects.create(
            user=self.user,
            title='OK',
            description='Hola',
            daily_goal=2 
        )
        self.mission1 = DailyMission.objects.create(
            title='okokok',
            target=self.target1
        )

    def test_daily_mission_creation(self):
        self.assertEqual(self.mission1.target.daily_goal, self.target1.daily_goal)
        self.assertEqual(self.mission1.title, 'okokok')
        self.assertEqual(str(self.mission1), f"{self.mission1.title} - {self.mission1.target.title} ({self.mission1.status})")


class DailyMissionWordTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='mobin', password='Aa1100')

        self.word1 = Word.objects.create(name='hello', definition='A greeting', category='SHORT')
        self.word2 = Word.objects.create(name='By', definition='A greeting', category='SHORT')

        self.target1 = LearningTarget.objects.create(
            user=self.user,
            title='OK',
            description='Hola',
            daily_goal=2 
        )
        self.mission1 = DailyMission.objects.create(
            title='okokok',
            target=self.target1
        )
        self.word1_mission1 = DailyMissionWord.objects.create(
            daily_mission=self.mission1,
            word=self.word1
        )
    
    def test_daily_mission_word_creation(self):
        self.assertEqual(self.word1_mission1.daily_mission, self.mission1)
        self.assertEqual(self.word1_mission1.word.name, self.word1.name)
        self.assertEqual(str(self.word1_mission1), f"{self.word1_mission1.daily_mission.title} - {self.word1_mission1.word.name}")

    def test_unique_together(self):

        with self.assertRaises(IntegrityError):
            DailyMissionWord.objects.create(
                daily_mission=self.mission1,
                word=self.word1
        )

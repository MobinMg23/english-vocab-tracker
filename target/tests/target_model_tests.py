from django.test import TestCase
from target.models import LearningTarget
from django.contrib.auth import get_user_model

User = get_user_model()

class LearningTargetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='mobin23')
        self.user.set_password('okokok23')
        self.user.save()
        
        self.target1 = LearningTarget.objects.create(
            user=self.user,
            title='OK',
            description='Hola',
            daily_goal=2 
        )
    
    def test_create_learning_target(self):

        self.assertTrue(isinstance(self.target1, LearningTarget))
        self.assertEqual(self.target1.user.username, 'mobin23')
        self.assertEqual(self.target1.daily_goal, 2)
        self.assertNotEqual(self.target1.title, 'NO')
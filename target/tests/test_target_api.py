from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from target.models import LearningTarget
from django.urls import reverse 
from django.contrib.auth import get_user_model

User = get_user_model()



class LearningTargetAPIViewTests(APITestCase):
    def setUp(self):
        self.user = self.user = User.objects.create(username='mobin23')
        self.user.set_password('okokok23')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('target-create')

        self.target1 = LearningTarget.objects.create(
            user=self.user,
            title='OK',
            description='Hola',
            daily_goal=2 
        )
    
    def test_post_create_target(self):
        response = self.client.post(self.url, 
            {
                'title': 'OK',
                'description': 'Hola',
                'daily_goal': 2 
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.target1, LearningTarget.objects.all())
        self.assertEqual(response.data['title'], 'OK')

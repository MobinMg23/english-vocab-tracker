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


class LearningTargetDetailAPIViewTests(APITestCase):
    def setUp(self):
        self.user = self.user = User.objects.create(username='mobin23')
        self.user.set_password('okokok23')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.target1 = LearningTarget.objects.create(
            user=self.user,
            title='OK',
            description='Hola',
            daily_goal=2 
        )
        self.target2 = LearningTarget.objects.create(
            user=self.user,
            title='No',
            description='Halo',
            daily_goal=3
        )

        self.url = reverse('target-detail', kwargs={"pk": self.target1.id})

    def test_get_target_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.target1.title, response.data['title'])

    def test_get_target_detail_404error(self):
        self.url = reverse('target-detail', kwargs={'pk': 10})
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_target_detail(self):
        response = self.client.patch(self.url,
        {
            'title': 'Yes You Can'
        }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.target1.title, response.data['title'])
    
    def test_patch_target_detail_404error(self):
        self.url = reverse('target-detail', kwargs={'pk': 10})
        response = self.client.patch(self.url, 
        {
            'title': 'Yes You Can'
        }, format='multipart')
        
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_target_detail_500error(self):
        response = self.client.patch(self.url, 
        {
            'daily_goal': 'Yes'
        }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from target.models import LearningTarget
from django.urls import reverse 
from django.contrib.auth import get_user_model

User = get_user_model()



class IsOwnerPermissionTests(APITestCase):
    def setUp(self):

        self.owner_user = User.objects.create(username='owner', password='okokok')
        self.other_user = User.objects.create(username='vini', password='jr')
        self.client = APIClient()
        self.client.force_authenticate(user=self.owner_user)

        self.target = LearningTarget.objects.create(
            user=self.owner_user,
            title='Test Target',
            daily_goal=5
        )

        self.url = reverse("target-detail", kwargs={'pk': self.target.id})

    def test_owner_can_access(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_owner(self):
        self.client.force_login(user=self.other_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

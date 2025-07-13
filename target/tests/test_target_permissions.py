from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from target.models import LearningTarget
from django.urls import reverse 
from django.contrib.auth import get_user_model

User = get_user_model()


def create_user_jwt_token(user):
    refresh = RefreshToken.for_user(user=user)
    return str(refresh.access_token)


class IsOwnerPermissionTests(APITestCase):
    def setUp(self):

        self.owner_user = User.objects.create_user(username='owner', password='okokok')
        self.other_user = User.objects.create_user(username='vini', password='jr')

        self.target = LearningTarget.objects.create(
            user=self.owner_user,
            title='Test Target',
            daily_goal=5
        )

        self.url = reverse("target-detail", kwargs={'pk': self.target.id})

    def test_owner_can_access(self):
        token = create_user_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_owner(self):
        token = create_user_jwt_token(self.other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

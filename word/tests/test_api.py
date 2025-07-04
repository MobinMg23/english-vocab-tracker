import io
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse 


User = get_user_model()



class WordSaveAPIViewTests(APITestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(username='mobin', defaults={'is_staff': True})
        self.user.set_password('12345Mm')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('word-save')

    @patch('word.views.word_save_task.apply_async')
    def test_post(self, mock_apply_async):
        text = 'hello\ngod\nworld'
        file = io.BytesIO(text.encode('utf-8'))
        file.name = 'word-list.txt'
        
        response = self.client.post(self.url,
            {
                'file': file,
                'category': 'short'
            }, format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(mock_apply_async.call_count, 3)
        called_args = [call.kwargs['args'] for call in mock_apply_async.call_args_list]
        self.assertIn(['short', 'hello'], called_args)
        self.assertIn(['short', 'god'], called_args)
        self.assertIn(['short', 'world'], called_args)
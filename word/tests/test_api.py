import io
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse 
from django.http import Http404
from word.models import Word


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
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(mock_apply_async.call_count, 3)
        called_args = [call.kwargs['args'] for call in mock_apply_async.call_args_list]
        self.assertIn(['short', 'hello'], called_args)
        self.assertIn(['short', 'god'], called_args)
        self.assertIn(['short', 'world'], called_args)

    @patch('word.views.word_save_task.apply_async')
    def test_post_withoput_file(self, mock_apply_async):
        response = self.client.post(self.url, {'category': 'short'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_apply_async.assert_not_called()

    @patch('word.views.word_save_task.apply_async')
    def test_post_empty_file(self, mock_apply_async):
        file = io.BytesIO(b'')
        file.name = 'file.txt'
        
        response = self.client.post(self.url, {
            'category': 'short',
            'file': file
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WordListAPIViewTests(APITestCase):
    def setUp(self):
        self.word1 =  Word.objects.create(name='hello', definition='A greeting', category='SHORT')
        self.word2 =  Word.objects.create(name='mobin', definition='A greeting', category='SHORT')
        self.client = APIClient()
        self.url = reverse('word-list')

    def test_get_queryset(self):
        response = self.client.get(self.url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST])
        self.assertEqual([obj['name'] for obj in data], [name for name in [self.word1.name, self.word2.name]])


class WordDetailAPIViewTests(APITestCase):
    def setUp(self):
        self.word1 =  Word.objects.create(name='hello', definition='A greeting', category='SHORT')
        self.word2 =  Word.objects.create(name='mobin', definition='A greeting', category='SHORT')

        self.user = User.objects.create(username='mobin')
        self.user.set_password('112234M')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.url = '/api/word/detail'

    def test_get_detail(self):
        response = self.client.get(f'{self.url}/{self.word1.name}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.word1.name)

    def test_get_detail_not_found(self):
        word = 'ali'
        response = self.client.get(f'{self.url}/{word}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        
        
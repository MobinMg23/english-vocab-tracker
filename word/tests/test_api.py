import io
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse 
from django.http import Http404
from word.models import Word, Translation, LearnedWord
from word.views import WordTranslateAPIView
from target.models import LearningTarget


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
                'category': 'SHORT'
            }, format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(mock_apply_async.call_count, 3)
        called_args = [call.kwargs['args'] for call in mock_apply_async.call_args_list]
        self.assertIn(['SHORT', 'hello'], called_args)
        self.assertIn(['SHORT', 'god'], called_args)
        self.assertIn(['SHORT', 'world'], called_args)

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

        
class WordTranslateAPIViewTests(APITestCase):
    def setUp(self):
        self.word1 = Word.objects.create(name='hello', definition='A greeting', category='SHORT')

        self.translation1 = Translation.objects.create(
            word=self.word1,
            word_translation='سلام',
            example_translation='سلام به شما',
            language='fa'
        )

        self.user = User.objects.create(username='mobin', is_staff=True)
        self.user.set_password('1122Mn')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.url = reverse('word-translate', kwargs={'language': 'fa'})
    
    def test_get_queryset(self):
        view = WordTranslateAPIView()
        view.kwargs = {'language': 'fa'}
        queryset = view.get_queryset()

        self.assertNotIn(self.word1, queryset)    

    @patch('word.views.word_translate_task.apply_async')
    def test_word_translate(self, mock_apply_async):
        self.url = reverse('word-translate', kwargs={'language': 'es'})
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(mock_apply_async.call_count, 1)
        called_args = [call.kwargs['args'] for call in mock_apply_async.call_args_list]
        self.assertIn([self.word1.id, 'es'], called_args)

    @patch('word.views.word_translate_task.apply_async')
    def test_not_found_word_translate(self, mock_apply_async):

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        mock_apply_async.assert_not_called()


class WordTranslateDetailAPIViewTests(APITestCase):
    def setUp(self):
        self.word1 = Word.objects.create(name='hello', definition='A greeting', category='SHORT')

        self.translation1 = Translation.objects.create(
            word=self.word1,
            word_translation='سلام',
            example_translation='سلام به شما',
            language='fa'
        )

        self.user = User.objects.create(username='mobin')
        self.user.set_password('1122Mn')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.url = reverse('word-translate-detail', kwargs={
            'language': 'fa',
            'word': 'hello'
        })

    def test_get_translate_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.translation1.word_translation, response.data['word_translation'])

    def test_not_found_translate_detail(self):
        self.url = reverse('word-translate-detail', kwargs={
            'language': 'es',
            'word': 'hello'
        })

        response = self.client.get(self.url)
        
        self.assertFalse(Translation.objects.filter(word__name='hello', language='es').exists())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LearnedWordListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='mobin')
        self.user.set_password('mobin1133')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('leaned-word-list')

        self.word1 = Word.objects.create(name='hello', definition='A greeting', category='SHORT')
        self.target1 = LearningTarget.objects.create(user=self.user, title='never give up', daily_goal=2)
        self.learned_word = LearnedWord.objects.create(user=self.user, target=self.target1, word=self.word1)

    def test_get_list(self):
        response = self.client.get(self.url)
        print(response.data)
        word_ids = [learned['id'] for learned in response.data]
        word_names = [learned['word_name'] for learned in response.data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.word1.id, word_ids)
        self.assertIn(self.word1.name, word_names)
        
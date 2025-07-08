from django.test import TestCase
from django.db import IntegrityError
from word.models import Word, Translation, LearnedWord
from target.models import LearningTarget
from authentication.models import User



class WordModelTest(TestCase):
    def setUp(self):
        self.word = Word.objects.create(name='hello', definition='A greeting', category='SHORT')
        self.translation = Translation.objects.create(
            word=self.word,
            word_translation='سلام',
            example_translation='سلام به شما',
            language='fa'
        )   

    def test_word_creation(self):
        self.assertEqual(self.word.name, 'hello')
        self.assertEqual(self.word.definition, 'A greeting')
        self.assertEqual(self.word.category, 'SHORT')
        self.assertTrue(isinstance(self.word, Word))

    def test_get_category(self):
        self.assertEqual(self.word.get_category(), 'SHORT')
        self.assertFalse(self.word.get_category() == 'LONG')
        self.assertTrue(self.word.get_category() in ['SHORT', 'MEDIUM', 'LONG'])

    def test_word_str(self):
        self.assertEqual(str(self.word), 'hello')
        self.assertFalse(str(self.word) == 'hola')
        self.assertTrue('hello' in str(self.word.name))


class TranslationModelTest(TestCase):
    def setUp(self):
        self.word = Word.objects.create(name='hello', definition='A greeting', category='SHORT')
        self.translation = Translation.objects.create(
            word=self.word,
            word_translation='سلام',
            example_translation='سلام به شما',
            language='fa'
        )
        
    def test_translation_creation(self):
        self.assertEqual(self.translation.word_translation, 'سلام')
        self.assertEqual(self.translation.example_translation, 'سلام به شما')
        self.assertEqual(self.translation.language, 'fa')
        self.assertTrue(isinstance(self.translation, Translation))
        self.assertEqual(str(self.translation), 'سلام (fa)')
    
    def test_get_word_translation(self):
        translate = Translation.objects.get_word_translation(self.word, 'fa')
        self.assertEqual(translate[0], 'سلام')
        self.assertEqual(self.translation.example_translation, 'سلام به شما')
        self.assertFalse(self.translation.example_translation == 'hello')

    def test_get_example_translation(self):
        example = Translation.objects.get_example_translation(self.word, 'fa')
        self.assertEqual(example, 'سلام به شما')
        self.assertFalse(example == 'hello')
        self.assertTrue(isinstance(example, str))

    def test_translation_unique_together(self):
        with self.assertRaises(IntegrityError):
            Translation.objects.create(
                word=self.word,
                word_translation='سلام',
                example_translation='سلام به شما',
                language='fa'
            )


class LearnedWordModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='mobin', password='12345', email='mobin@gmail.com')
        self.target = LearningTarget.objects.create(user=self.user, title='Learn English', end_date='2024-12-31',
                                                     daily_goal=5, start_date='2024-01-01')
        self.word = Word.objects.create(name='hello', definition='A greeting', category='SHORT')
        self.learned_word = LearnedWord.objects.create(user=self.user, target=self.target, word=self.word)

    def test_learned_word_creation(self):
        self.assertEqual(self.user.username, 'mobin')
        self.assertEqual(self.target.title, 'Learn English')
        self.assertEqual(self.word.name, 'hello')
        self.assertTrue(isinstance(self.learned_word, LearnedWord))
        self.assertEqual(self.learned_word.word.name, 'hello')
        self.assertEqual(str(self.learned_word), 'hello - mobin')
        self.assertFalse(self.learned_word.user == 'moein')

    def test_learned_word_unique_together(self):
        with self.assertRaises(IntegrityError):
            LearnedWord.objects.create(user=self.user, target=self.target, word=self.word)


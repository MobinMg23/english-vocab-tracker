from celery import shared_task
from deep_translator import GoogleTranslator
from word.models import Word, Translation
import requests
import logging

logger = logging.getLogger(__name__)



def translate_text_deep_translator(text, target):
    if not text:
        return None
    return GoogleTranslator(source='auto', target=target).translate(text)


@shared_task(bind=True, name="word_translate_task", max_retries=3)
def word_translate_task(self, word_id, language):
    try:

        word = Word.objects.get(id=word_id)

        word_translation = translate_text_deep_translator(word.name, language)
        example_translation = translate_text_deep_translator(word.example, language) if word.example else None

        translation = Translation.objects.create(
            word=word,
            word_translation=word_translation,
            example_translation=example_translation,
            language=language
        )
        logger.info(f"Translation for word '{word.name}' in language '{language}' created successfully.")

    except Word.DoesNotExist:
        logger.error(f"Word with id {word_id} does not exist.")
        return 
    
    except requests.RequestException as e:
        logger.error(f"Request failed for word '{word.name}': {e}")
        raise self.retry(exc=e, countdown=60)
    
    except Exception as e:
        logger.error(f"An error occurred while translating word '{word.name}': {e}")
        raise self.retry(exc=e, countdown=60)
from celery import shared_task
import requests
import logging
from word.models import Word

logger = logging.getLogger(__name__)


@shared_task(bind=True, name="word_save_task", max_retries=3)
def word_save_task(self, category, word):

    try:

        already_exists = Word.objects.filter(name=word).exists()
        if already_exists:
            logger.info(f"Word '{word}' already exists in the database.")
            return

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)

        if response.status_code == 404:
            logger.warning(f"Word '{word}' not found in dictionary API.")
            return
            
        response.raise_for_status() 
        data = response.json()

        entry = data[0]
        meanings = entry.get('meanings', [])
        if not meanings:
            return

        definitions = meanings[0].get('definitions', [])
        if not definitions:
            return

        definition = definitions[0].get('definition', '')
        example = definitions[0].get('example', '')

        Word.objects.create(
            name=word,
            category=category,
            definition=definition,
            example=example,
        )
        logger.info(f"Word '{word}' saved successfully.")

    except requests.RequestException as e:
        logger.error(f"Request failed for word '{word}': {e}")
        raise self.retry(exc=e, countdown=60)
    except Exception as e:
        logger.error(f"An error occurred while saving word '{word}': {e}")
        raise self.retry(exc=e, countdown=60)

        

from celery import shared_task
from django.contrib.auth import get_user_model
import logging
from daily_mission.models import DailyMission, DailyMissionWord
from target.models import LearningTarget
from word.models import LearnedWord, Word
from celery_tasks.send_email.send_email_task import send_email


logger = logging.getLogger(__name__)

User = get_user_model()



@shared_task(bind=True, name='send_daily_mission_email_task')
def send_daily_mission_email(self, user_id):
    try:
        user = User.objects.get(id=user_id)

        subject = '🎯 ماموریت روزانه‌ات آماده‌ست!'
        message = f'سلام {user.first_name or user.username}!\nماموریت امروزت در دسترسه. بیا و تمرینت رو انجام بده 🌟'

        send_email(user.id, subject, message)
        logger.info(f'Sending daily mission email to user {user.email}')

    except User.DoesNotExist:
        logger.warning(f'User with id {user_id} does not exist')
    except Exception as e:
        logger.error(f'Unexpected error while sending email to user {user_id}: {e}')

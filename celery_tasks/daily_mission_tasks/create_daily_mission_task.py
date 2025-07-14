from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from random import randint, sample
import logging
from daily_mission.models import DailyMission, DailyMissionWord
from target.models import LearningTarget
from word.models import LearnedWord, Word
from celery_tasks.daily_mission_tasks.send_daily_mission_email_task import send_daily_mission_email
from django.db import transaction


User = get_user_model()


logger = logging.getLogger(__name__)


@shared_task(bind=True, name='create_daily_mission_tasks')
def create_daily_mission(self, user_id):
    today = timezone.now().date()

    try:
        targets = LearningTarget.objects.filter(user__id=user_id)
        created_count = 0
        delay_time = 3

        for target in targets:
            if DailyMission.objects.filter(target=target, datetime__date=today).exists():
                logger.info(f"Daily mission already exists for user: {target.user.username}")
                continue
            with transaction.atomic():
                mission = DailyMission.objects.create(
                    title=f"Daily mission {today}",
                    target=target
                )

                learned_words_ids = LearnedWord.objects.filter(
                    user=target.user
                ).values_list('word_id', flat=True)

                available_words = Word.objects.exclude(id__in=learned_words_ids)

                daily_goal = target.daily_goal

                available_words_list = list(available_words)
                if len(available_words_list) < daily_goal:
                    logger.warning(f"Not enough words for user: {target.user.username}")
                    continue

                selected_words = sample(available_words_list, daily_goal)

                daily_mission_words = [
                    DailyMissionWord(daily_mission=mission, word=word) for word in selected_words
                ]
                DailyMissionWord.objects.bulk_create(daily_mission_words)

                created_count += 1
                logger.info(f"✅ Created daily mission for user: {target.user.username}")

                #Send Daily Mission Email
                if target.user.email:
                    send_daily_mission_email.apply_async(kwargs={'user_id': target.user.id}, countdown=delay_time)
                    logger.info(f'Send Email for User: {target.user.username} -- Email: {target.user.email}')
                    delay_time += randint(1, 5) 
                else:
                    logger.warning(f"User {target.user.username} has no email, skipping email task.")

        return f"✅ Done. Total created: {created_count}"  
    
    except Exception as e:
        logger.error(f"❌ Error in create_daily_mission: {str(e)}")
        self.retry(exc=e, countdown=60, max_retries=3)

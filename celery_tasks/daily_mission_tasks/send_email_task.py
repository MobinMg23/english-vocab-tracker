from celery import shared_task



@shared_task
def send_daily_email(self, user_id):
    pass
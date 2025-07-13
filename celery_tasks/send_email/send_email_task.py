from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import os

User = get_user_model()


def send_email(user_id, subject, message):
    user = User.objects.get(id=user_id)

    subject = subject
    message = message
    from_email = os.getenv('FROM_EMAIL', '')
    recipient_list = [user.email]


    send_mail(
        subject,
          message,
            from_email,
              recipient_list
              )

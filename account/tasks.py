from celery import shared_task
from django.core.mail import send_mail
from My_WEB import settings
from .models import Profile


@shared_task
def send_welcome_email(user_id):
    user = Profile.objects.get(pk=user_id)
    subject = f'Welcome to {user.username}'
    message = f'Your account has been created'
    mail_sent = send_mail(subject,
                          message,
                          'matrix@gmail.com',
                          [user.email])
    return mail_sent

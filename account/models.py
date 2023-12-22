from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/',
                              blank=True,
                              default='users/no_image.jpg')
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False))


class Message(models.Model):
    sender = models.ForeignKey('auth.User',
                               related_name='rel_sender_set',
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey('auth.User',
                                 related_name='rel_receiver_set',
                                 on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['sent_at'])
        ]
        ordering = ['sent_at']

    def __str__(self):
        return f'{self.sender} send message {self.receiver}'

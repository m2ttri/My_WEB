from django.db import models
from django.conf import settings
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/',
                              blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

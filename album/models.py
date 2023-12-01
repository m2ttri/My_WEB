from django.db import models
from django.conf import settings
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Album.Status.PUBLIC)


class Album(models.Model):

    class Status(models.TextChoices):
        PRIVATE = 'PR', 'Private'
        PUBLIC = 'PB', 'Public'

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='album',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publish = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.PUBLIC)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='albums_liked',
                                        blank=True)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-update']
        indexes = [
            models.Index(fields=['-update']),
        ]

    def __str__(self):
        return self.title


class Image(models.Model):
    album = models.ForeignKey(Album,
                              related_name='images',
                              on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    add = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    album = models.ForeignKey(Album,
                              on_delete=models.CASCADE,
                              related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comments',
                             on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update']
        indexes = [
            models.Index(fields=['-update']),
        ]

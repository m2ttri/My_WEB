from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Album.Status.PUBLISHED)


class Album(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='album_created',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    publish = models.DateTimeField(default=timezone.now)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='album_liked',
                                        blank=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('album:album_list',
                       args=[self.slug])


class Image(models.Model):
    album = models.ForeignKey(Album,
                              related_name='images',
                              on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/',
                              blank=True)
    add = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('album:album_detail',
                       args=[self.id])

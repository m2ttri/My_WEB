from django.contrib import admin
from .models import Album, Image


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status']
    list_filter = ['publish', 'status']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['-status', '-publish']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['album', 'image', 'add']
    list_filter = ['add']
    ordering = ['-add']

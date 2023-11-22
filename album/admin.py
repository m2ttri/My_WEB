from django.contrib import admin
from .models import Album, Image


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'update', 'status', 'publish']
    list_filter = ['update', 'status']
    search_fields = ['author__username', 'title']
    raw_id_fields = ['author']
    ordering = ['-status', '-update']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['album', 'image', 'add']
    list_filter = ['add']
    ordering = ['-add']

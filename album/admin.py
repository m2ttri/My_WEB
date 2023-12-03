from django.contrib import admin
from .models import Album, Image, Comment


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'update', 'status', 'publish', 'total_likes']
    list_filter = ['update', 'status', 'total_likes']
    search_fields = ['author__username', 'title']
    raw_id_fields = ['author']
    ordering = ['-status', '-update']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['album', 'image', 'add']
    list_filter = ['add']
    ordering = ['-add']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['album', 'user', 'update']
    list_filter = ['update']
    search_fields = ['album', 'user', 'body']

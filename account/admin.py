from django.contrib import admin
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'created']
    list_filter = ['created']
    raw_id_fields = ['user']
    ordering = ['-created']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'sent_at']
    list_filter = ['sent_at']
    ordering = ['-sent_at']

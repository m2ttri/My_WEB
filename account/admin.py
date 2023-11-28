from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'created']
    list_filter = ['created']
    raw_id_fields = ['user']
    ordering = ['-created']

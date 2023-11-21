from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),
    path('register/', views.register, name='register'),
]

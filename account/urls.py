from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),
    path('register/', views.register, name='register'),
    path('user/follow/', views.user_follow, name='user_follow'),
    path('<username>/', views.user_detail, name='user_detail'),
    path('<username>/actions/', views.get_action, name='actions'),
]

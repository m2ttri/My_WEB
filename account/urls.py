from django.urls import path, include
from .views import CustomLoginView
from . import views


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),
    path('register/', views.register, name='register'),
    path('user/follow/', views.user_follow, name='user_follow'),
    path('<username>/', views.user_detail, name='user_detail'),
    path('<username>/actions/', views.get_action, name='actions'),
    path('<username>/messages/', views.send_message, name='messages'),
]

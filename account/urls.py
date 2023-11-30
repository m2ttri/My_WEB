from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),
    path('register/', views.register, name='register'),
    path('user/follow/', views.user_follow, name='user_follow'),
    path('user/<username>/', views.user_detail, name='user_detail'),

    # path('user/<int:user_id>/', views.user_albums, name='user_albums'),
]

from django.urls import path, include
from . import views
from .views import UserProfileDetailVIew


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),
    path('register/', views.register, name='register'),
    path('user/<int:user_id>/', UserProfileDetailVIew.as_view(), name='user_profile'),
]

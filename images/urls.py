from django.urls import path
from . import views


app_name = 'album'

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('<int:id>/', views.album_detail, name='album_detail'),
]

from django.urls import path
from .views import AlbumDeleteView
from . import views


app_name = 'album'

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('<int:id>/', views.album_detail, name='album_detail'),
    path('create/', views.create_album, name='album_create'),
    path('<int:id>/edit/', views.edit_album, name='album_edit'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name="album_delete"),
]

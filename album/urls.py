from django.urls import path
from .views import AlbumDeleteView, ImageDeleteView
from . import views


app_name = 'album'

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('create/', views.create_album, name='album_create'),
    path('<int:id>/', views.album_detail, name='album_detail'),
    path('<int:id>/edit/', views.edit_album, name='album_edit'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
    path('image/<int:pk>/delete/', ImageDeleteView.as_view(), name='image_delete'),
    path('image/<int:image_id>/download', views.download_image, name='image_download'),
]

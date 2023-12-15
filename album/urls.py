from django.urls import path
from .views import AlbumDeleteView, ImageDeleteView, CommentDeleteView, AlbumDetailView
from . import views


app_name = 'album'

urlpatterns = [
    path('create/', views.create_album, name='album_create'),
    path('<int:id>/images/', AlbumDetailView.as_view(), name='album_detail'),
    path('<int:id>/edit/', views.edit_album, name='album_edit'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
    path('image/<int:pk>/delete/', ImageDeleteView.as_view(), name='image_delete'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
    path('image/<int:image_id>/download', views.download_image, name='image_download'),
    path('album/<int:album_id>/download', views.download_album, name='album_download'),
    path('like/', views.album_like, name='like'),
    path('search/', views.album_search, name='album_search'),
]

from django.urls import path
from . import views


app_name = 'album'

urlpatterns = [
    path('albums/',
         views.AlbumListView.as_view(),
         name='album_list'),
    path('albums/<pk>/',
         views.AlbumDetailView.as_view(),
         name='album_detail'),
]

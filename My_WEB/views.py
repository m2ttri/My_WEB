from django.shortcuts import render
from album.models import Album


def index(request):
    albums = Album.published.all()
    return render(request,
                  'index.html',
                  {'albums': albums})

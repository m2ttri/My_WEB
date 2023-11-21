from django.shortcuts import render, get_object_or_404
from .models import Album, Image


def album_list(request, album_slug=None,):
    album = None
    albums = Album.published.all()
    images = Image.objects.all()
    if album_slug:
        album = get_object_or_404(Album,
                                  slug=album_slug)
        images = images.filter(album=album)
    return render(request,
                  'album/list.html',
                  {'album': album,
                   'albums': albums,
                   'images': images})


def album_detail(request, id):
    album = get_object_or_404(Album,
                              id=id,
                              status=Album.Status.PUBLISHED)
    return render(request,
                  'album/detail.html',
                  {'album': album})

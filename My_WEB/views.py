from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from album.models import Album
from album.views import r


def index(request):
    albums = Album.published.all()
    for album in albums:
        album.total_views = r.get(f'album:{album.id}:views').decode()
    paginator = Paginator(albums, 10)
    page = request.GET.get('page')
    albums_only = request.GET.get('albums_only')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        if albums_only:
            return HttpResponse('')
        albums = paginator.page(paginator.num_pages)
    if albums_only:
        return render(request,
                      'album/list.html',
                      {'albums': albums})
    return render(request,
                  'index.html',
                  {'albums': albums})

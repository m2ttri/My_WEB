from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from album.models import Album


def index(request):
    albums = Album.published.all()
    paginator = Paginator(albums, 8)
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


# def index(request):
#     albums = Album.published.all()
#     paginator = Paginator(albums, 8)
#     page_number = request.GET.get('page', 1)
#     posts = paginator.page(page_number)
#     return render(request,
#                   'index.html',
#                   {'posts': posts})

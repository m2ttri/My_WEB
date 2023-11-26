from django.shortcuts import render
from album.models import Album
from django.core.paginator import Paginator


def index(request):
    albums = Album.published.all()
    paginator = Paginator(albums, 8)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    return render(request,
                  'index.html',
                  {'posts': posts})

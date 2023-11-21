from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Album, Image
from .forms import AlbumForm, AlbumEditForm, ImageForm
from django.core.paginator import Paginator


@login_required
def album_list(request):
    albums = Album.objects.filter(author=request.user)
    paginator = Paginator(albums, 6)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    return render(request,
                  'album/list.html',
                  {'posts': posts})


def album_detail(request, id):
    album = get_object_or_404(Album, id=id)
    return render(request,
                  'album/detail.html',
                  {'album': album})


@login_required()
def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        image = ImageForm(request.POST,
                          request.FILES)
        if form.is_valid() and image.is_valid():
            album = form.save(commit=False)
            album.author = request.user
            album.save()
            for file in request.FILES.getlist('images'):
                Image.objects.create(album=album, image=file)
            return redirect('album:album_detail', album.id)
    else:
        form = AlbumForm()
        image = ImageForm()
    return render(request,
                  'album/create.html',
                  {'form': form, 'image': image})


@login_required
def edit_album(request, id):
    album = get_object_or_404(Album, id=id)
    if request.method == 'POST':
        form = AlbumEditForm(instance=album,
                             data=request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.author = request.user
            album.save()
            return redirect('album:album_list')
    else:
        form = AlbumEditForm(instance=album)
    return render(request, 'album/edit.html',
                  {'form': form, 'album': album})

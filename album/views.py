from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Album
from .forms import AlbumForm, AlbumEditForm, ImageForm


def album_detail(request, id):
    album = get_object_or_404(Album, id=id)
    if request.method == 'POST':
        add_image_form = ImageForm(request.POST,
                                   request.FILES)
        if add_image_form.is_valid():
            images = add_image_form.save(commit=False)
            images.album = album
            images.save()
            return redirect('album:album_detail', album.id)
    else:
        add_image_form = ImageForm()
    return render(request,
                  'album/detail.html',
                  {'album': album, 'add_image_form': add_image_form})


@login_required
def album_list(request):
    albums = Album.objects.filter(author=request.user)
    paginator = Paginator(albums, 6)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    return render(request,
                  'album/list.html',
                  {'posts': posts})


@login_required()
def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.author = request.user
            album.save()
            return redirect('album:album_detail', album.id)
    else:
        form = AlbumForm()
    return render(request,
                  'album/create.html',
                  {'form': form})


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


# @login_required
# def add_images(request, id):
#     album = get_object_or_404(Album, id=id)
#     if request.method == 'POST':
#         form = ImageForm(request.POST,
#                          request.FILES)
#         if form.is_valid():
#             images = form.save(commit=False)
#             images.album = album
#             images.save()
#             return redirect('album:album_detail', album.id)
#     else:
#         form = ImageForm()
#     return render(request,
#                   'album/add_images_form.html',
#                   {'form': form, 'album': album})

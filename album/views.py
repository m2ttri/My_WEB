import os
import redis
import zipfile
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic.edit import DeleteView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import FileResponse, JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
from .forms import AlbumForm, AlbumEditForm, MultipleImageForm, SearchForm, CommentForm
from .models import Album, Image, Comment

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


def comment_form(request, album):
    """Форма для добавления комментариев"""
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.album = album
            comment.user = request.user
            comment.save()
            return form, True
    else:
        form = CommentForm()
    return form, False


def album_detail(request, id):
    """Детальное отображение альбома"""
    album = get_object_or_404(Album, id=id)
    images = album.images.all()
    total_views = r.incr(f'album:{album.id}:views')
    paginator = Paginator(images, 10)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(
            request,
            'album/images_list.html',
            {'images': images}
        )

    comments = Comment.objects.filter(album=album)
    form, is_redirect = comment_form(request, album)
    if is_redirect:
        return redirect('album:album_detail', album.id)
    context = {
        'images': images,
        'album': album,
        'total_views': total_views,
        'comment_form': form,
        'comments': comments
    }
    if album.status == 'PR' and request.user != album.author:
        return redirect('/')
    else:
        return render(
            request,
            'album/detail.html',
            context
        )


@login_required
def edit_album(request, id):
    """Форма редактирования альбома"""
    album = get_object_or_404(Album, id=id)
    if request.method == "POST":
        form = AlbumEditForm(
            instance=album,
            data=request.POST
        )
        add_image_form = MultipleImageForm(
            request.POST,
            request.FILES
        )
        if form.is_valid() and add_image_form.is_valid():
            album = form.save(commit=False)
            album.author = request.user
            album.save()
            for image in request.FILES.getlist("images"):
                Image.objects.create(
                    image=image,
                    album=album
                )
            album = Album.objects.get(id=id)
            return redirect(
                "album:album_detail",
                album.id
            )
    else:
        form = AlbumEditForm(instance=album)
        add_image_form = MultipleImageForm()
    return render(
        request,
        'album/edit.html',
        {
            'form': form,
            'album': album,
            'add_image_form': add_image_form
        }
    )


@login_required
@require_POST
def album_like(request):
    album_id = request.POST.get('id')
    action = request.POST.get('action')
    if album_id and action:
        try:
            album = Album.objects.get(id=album_id)
            if action == 'like':
                album.users_like.add(request.user)
            else:
                album.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required()
def create_album(request):
    """Форма создания альбома"""
    if request.method == "POST":
        form = AlbumForm(request.POST)
        image_form = MultipleImageForm(
            request.POST,
            request.FILES
        )
        if form.is_valid() and image_form.is_valid():
            album = form.save(commit=False)
            album.author = request.user
            album.save()
            create_action(
                request.user,
                'create album',
                album
            )
            for image in request.FILES.getlist("images"):
                Image.objects.create(
                    image=image,
                    album=album
                )
            return redirect(
                "album:album_detail",
                album.id
            )
    else:
        form = AlbumForm()
        image_form = MultipleImageForm()
    return render(
        request,
        "album/create.html",
        {
            "form": form,
            "image_form": image_form
        }
    )


def album_search(request):
    """Поиск по названию альбома"""
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title')
            search_query = SearchQuery(query)
            results = Album.published.annotate(
                search=search_vector,
                rank=SearchRank(
                    search_vector,
                    search_query
                )
            ).filter(search=search_query).order_by('-rank')
            for album in results:
                album.total_views = r.get(f'album:{album.id}:views').decode()
            return render(
                request,
                'album/search.html',
                {
                    'query': query,
                    'results': results
                }
            )
    return render(
        request,
        'base.html',
        {'form': form}
    )


class AlbumDeleteView(DeleteView):
    """Удалить альбом"""
    model = Album
    template_name = "album/album_delete.html"

    def dispatch(self, request, *args, **kwargs):
        album = self.get_object()
        if album.author != request.user:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            "user_detail",
            kwargs={'username': self.object.author}
        )


class ImageDeleteView(DeleteView):
    """Удалить изображение"""
    model = Image

    def get_success_url(self):
        return reverse(
            'album:album_detail',
            kwargs={'id': self.object.album.id}
        )


class CommentDeleteView(DeleteView):
    """Удалить комментарий"""
    model = Comment

    def get_success_url(self):
        return reverse(
            'album:album_detail',
            kwargs={'id': self.object.album.id}
        )


def create_zip(album):
    """Заархивировать альбом"""
    zip_file_name = f'{album.title.replace(" ", "_")}.zip'
    zip_file_path = os.path.join(
        settings.MEDIA_ROOT,
        zip_file_name
    )
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for image in album.images.all():
            image_path = os.path.join(
                settings.MEDIA_ROOT,
                str(image.image)
            )
            zipf.write(
                image_path,
                arcname=os.path.basename(image_path)
            )
    return zip_file_path


def download_image(request, image_id):
    """Скачать изображение"""
    img = Image.objects.get(id=image_id)
    response = FileResponse(
        open(img.image.path, 'rb'),
        as_attachment=True
    )
    return response


def download_album(request, album_id):
    """Скачать альбом"""
    album = Album.objects.get(id=album_id)
    zip_file = create_zip(album)
    response = FileResponse(
        open(zip_file, 'rb'),
        as_attachment=True
    )
    return response

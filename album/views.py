from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator
from django.http import FileResponse, JsonResponse
from django.contrib.postgres.search import TrigramSimilarity
from .forms import AlbumForm, AlbumEditForm, MultipleImageForm, SearchForm
from .models import Album, Image


def album_detail(request, id):
    album = get_object_or_404(Album, id=id)
    if request.method == "POST":
        add_image_form = MultipleImageForm(request.POST,
                                           request.FILES)
        if add_image_form.is_valid():
            for image in request.FILES.getlist("images"):
                Image.objects.create(image=image,
                                     album=album)
            album = Album.objects.get(id=id)
            album.save()
            return redirect("album:album_detail",
                            album.id)
    else:
        add_image_form = MultipleImageForm()
    return render(request,
                  "album/detail.html",
                  {"album": album, "add_image_form": add_image_form})


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
    if request.method == "POST":
        form = AlbumForm(request.POST)
        image_form = MultipleImageForm(request.POST,
                                       request.FILES)
        if form.is_valid() and image_form.is_valid():
            album = form.save(commit=False)
            album.author = request.user
            album.save()
            for image in request.FILES.getlist("images"):
                Image.objects.create(image=image,
                                     album=album)
            return redirect("album:album_detail",
                            album.id)
    else:
        form = AlbumForm()
        image_form = MultipleImageForm()
    return render(request,
                  "album/create.html",
                  {"form": form, "image_form": image_form})


@login_required
def edit_album(request, id):
    album = get_object_or_404(Album, id=id)
    if request.method == "POST":
        form = AlbumEditForm(instance=album,
                             data=request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.author = request.user
            album.save()
            return redirect("album:album_list")
    else:
        form = AlbumEditForm(instance=album)
    return render(request,
                  "album/edit.html",
                  {"form": form, "album": album})


@login_required
def album_list(request):
    albums = Album.objects.filter(author=request.user)
    paginator = Paginator(albums, 8)
    page_number = request.GET.get("page", 1)
    posts = paginator.page(page_number)
    return render(request,
                  "album/list.html",
                  {"posts": posts})


def album_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Album.published.annotate(
                similarity=TrigramSimilarity('title', query), ).filter(
                similarity__gt=0.1).order_by('-similarity')
            return render(request,
                          'album/search.html',
                          {'form': form, 'query': query, 'results': results})
    return render(request,
                  'base.html',
                  {'form': form, 'query': query, 'results': results})


def download_image(request, image_id):
    img = Image.objects.get(id=image_id)
    response = FileResponse(open(img.image.path, 'rb'), as_attachment=True)
    return response


class AlbumDeleteView(DeleteView):
    model = Album
    template_name = "album/album_delete.html"

    def dispatch(self, request, *args, **kwargs):
        album = self.get_object()
        if album.author != request.user:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("album:album_list")


class ImageDeleteView(DeleteView):
    model = Image

    def get_success_url(self):
        return reverse('album:album_detail',
                       kwargs={'id': self.object.album.id})


# @require_POST
# def album_comment(request, id):
#     album = get_object_or_404(Album,
#                               id=id,
#                               status=Album.Status.PUBLIC)
#     comment = None
#     form = CommentForm(data=request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.album = album
#         comment.save()
#     return render(request, 'album/detail.html',
#                   {'album': album,
#                    'form': form,
#                    'comment': comment})
    

# @login_required
# def album_list(request):
#     albums = Album.objects.filter(author=request.user)
#     paginator = Paginator(albums, 8)
#     page = request.GET.get("page")
#     albums_only = request.GET.get('albums_only')
#     try:
#         albums = paginator.page(page)
#     except PageNotAnInteger:
#         albums = paginator.page(1)
#     except EmptyPage:
#         if albums_only:
#             return HttpResponse('')
#         albums = paginator.page(paginator.num_pages)
#     if albums_only:
#         return render(request, "album/list.html", {"albums": albums})
#     return render(request, "album/js_list.html", {"albums": albums})

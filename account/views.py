from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from album.models import Album
from .models import Profile, Contact
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from actions.utils import create_action
from actions.models import Action
from album.views import r


def update_total_likes(album):
    album.total_likes = album.users_like.count()


def get_total_likes(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    albums = Album.objects.filter(author=user).all()
    for album in albums:
        update_total_likes(album)
    sum_likes = sum(album.total_likes for album in albums)
    return sum_likes


def get_total_views(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    albums = Album.objects.filter(author=user).all()
    total_views = sum(int(r.get(f'album:{album.id}:views').decode()) for album in albums)
    return total_views


@login_required
def get_action(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    if request.user.is_authenticated:
        following_ids = request.user.following.values_list('id',
                                                           flat=True)
        actions = Action.objects.exclude(user=request.user).filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')
    else:
        actions = Action.objects.none()
    return render(request, 'actions/detail.html', {'user': user, 'actions': actions})


def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    albums = Album.objects.filter(author=user).all()
    for album in albums:
        album.total_views = r.get(f'album:{album.id}:views').decode()
    paginator = Paginator(albums, 8)
    page = request.GET.get('page')
    albums_only = request.GET.get('albums_only')
    sum_likes = get_total_likes(request, username)
    total_views = get_total_views(request, username)
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
                      'account/user_albums_list.html',
                      {'user': user,
                       'albums': albums})
    return render(request,
                  'account/user_profile.html',
                  {'user': user,
                   'albums': albums,
                   'sum_likes': sum_likes,
                   'total_views': total_views})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, new_user)
            return redirect('edit')
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated')
            return redirect('edit')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'is_following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

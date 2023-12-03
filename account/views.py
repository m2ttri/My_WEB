from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from album.models import Album
from .models import Profile, Contact
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from actions.utils import create_action
from actions.models import Action


def get_action(request):
    if request.user.is_authenticated:
        following_ids = request.user.following.values_list('id', flat=True)
        actions = Action.objects.exclude(user=request.user).filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')
    else:
        actions = Action.objects.none()
    return actions


def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    albums = Album.objects.filter(author=user).all()
    paginator = Paginator(albums, 8)
    page = request.GET.get('page')
    albums_only = request.GET.get('albums_only')
    actions = get_action(request)
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
                      {'user': user, 'albums': albums})
    return render(request,
                  'account/user_profile.html',
                  {'user': user, 'albums': albums, 'actions': actions})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
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
            return redirect('edit')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})


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


# @login_required
# def user_detail(request, username):
#     actions = Action.objects.exclude(user=request.user)
#     following_ids = request.user.following.values_list('id',
#                                                        flat=True)
#     if following_ids:
#         actions = actions.filter(user_id__in=following_ids)
#     actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
#     user = get_object_or_404(User,
#                              username=username,
#                              is_active=True)
#     albums_all = Album.objects.filter(author=user).all()
#     albums_pub = Album.published.filter(author=user).all()
#     paginator_all = Paginator(albums_all, 8)
#     paginator_pub = Paginator(albums_pub, 8)
#     page = request.GET.get('page')
#     albums_only = request.GET.get('albums_only')
#     try:
#         albums_all = paginator_all.page(page)
#         albums_pub = paginator_pub.page(page)
#     except PageNotAnInteger:
#         albums_all = paginator_all.page(1)
#         albums_pub = paginator_pub.page(1)
#     except EmptyPage:
#         if albums_only:
#             return HttpResponse('')
#         albums_all = paginator_all.page(paginator_all.num_pages)
#         albums_pub = paginator_pub.page(paginator_pub.num_pages)
#     if albums_only:
#         return render(request,
#                       'account/user_albums_list.html',
#                       {'user': user, 'albums_all': albums_all, 'albums_pub': albums_pub})
#     return render(request,
#                   'account/user_profile.html',
#                   {'user': user, 'albums_all': albums_all, 'albums_pub': albums_pub, 'actions': actions})

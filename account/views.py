from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from album.models import Album
from actions.models import Action
from album.views import r
from .models import Profile, Contact, Message
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, CustomAuthenticationForm, MessageForm

# from .tasks import send_welcome_email


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


@login_required
def send_message(request, username):
    """Отправка сообщений между пользователями"""
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    messages = Message.objects.filter(Q(sender=user, receiver=request.user) | Q(sender=request.user, receiver=user))
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = user
            message.save()
            return redirect('messages', user)
    else:
        form = MessageForm()
    return render(request,
                  'account/message_form.html',
                  {'form': form, 'user': user, 'messages': messages})


@login_required
def get_action(request, username):
    """Отслеживание действий пользователей"""
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    if request.user.is_authenticated:
        following_ids = request.user.following.values_list('id',
                                                           flat=True)
        actions = Action.objects.exclude(
            user=request.user).filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')
    else:
        actions = Action.objects.none()
    return render(request,
                  'actions/detail.html',
                  {'user': user, 'actions': actions})


def user_detail(request, username):
    """Отображение страницы пользователя с созданными альбомами"""
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    albums = Album.objects.filter(author=user).all()
    for album in albums:
        album.total_views = r.get(f'album:{album.id}:views').decode()
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
                      'account/user_albums_list.html',
                      {'user': user, 'albums': albums})
    return render(request,
                  'account/user_profile.html',
                  {'user': user, 'albums': albums})


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            # send_welcome_email.delay(new_user.id)
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
    """Редактирование профиля"""
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
    """Подписка на пользователя"""
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(
                    user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from album.models import Album
from .models import Profile, Contact
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm


# from actions.utils import create_action
# from actions.models import Action


def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    albums_all = Album.objects.filter(author=user).all()
    albums_pub = Album.published.filter(author=user).all()
    return render(request,
                  'account/user_profile.html',
                  {'user': user, 'albums_all': albums_all, 'albums_pub': albums_pub})


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
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


# def users_actions(request):
#     actions = Action.objects.exclude(user=request.user)
#     following_ids = request.user.following.values_list('id', flat=True)
#     if following_ids:
#         actions = actions.filter(user_id__in=following_ids)
#     actions = actions.select_related('user', 'user__profile')[:10].prefetch_related('target')[:10]
#     return render(request,
#                   'account/user_profile.html',
#                   {'actions': actions})

# from django.core.paginator import Paginator
# def user_albums(request, user_id):
#     profile = Profile.objects.get(user__id=user_id)
#     albums = Album.published.filter(author=profile.user).all()
#     paginator = Paginator(albums, 8)
#     page_number = request.GET.get("page", 1)
#     posts = paginator.page(page_number)
#     context = {'posts': posts, 'profile': profile}
#     return render(request, 'account/user_profile.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from album.models import Album
from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm


def user_albums(request, user_id):
    profile = Profile.objects.get(user__id=user_id)
    albums = Album.published.filter(author=profile.user).all()
    paginator = Paginator(albums, 8)
    page_number = request.GET.get("page", 1)
    posts = paginator.page(page_number)
    context = {'posts': posts, 'profile': profile}
    return render(request, 'account/user_profile.html', context)


# from django.views.generic import DetailView
# class UserProfileDetailVIew(DetailView):
#     model = Profile
#     template_name = 'account/user_profile.html'
#     context_object_name = 'profile'
#     slug_field = 'user_id'
#     slug_url_kwarg = 'user_id'


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

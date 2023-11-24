from django import forms
from .models import Album, Image


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'status']


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image']


class AlbumEditForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'status']

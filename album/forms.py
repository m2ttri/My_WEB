from django import forms
from .models import Album, Image


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'status']

    def clean_title(self):
        data = self.cleaned_data['title']
        if Album.objects.filter(title=data).exists():
            raise forms.ValidationError('Title already in use')
        return data


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image']


class AlbumEditForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'status']

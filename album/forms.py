from django import forms
from django.forms import ClearableFileInput, FileField
from .models import Album, Image, Comment


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'status']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='Write a comment',
                           widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))

    class Meta:
        model = Comment
        fields = ['body']


class AlbumEditForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'status']


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultipleImageForm(forms.Form):
    images = MultipleFileField(widget=MultipleFileInput(attrs={'multiple': True}),
                               required=False)


class SearchForm(forms.Form):
    query = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'placeholder': 'Search'}))

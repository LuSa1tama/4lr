from django import forms
from .models import Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'release_year', 'genre', 'duration']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'artist': forms.TextInput(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': "Название альбома",
            'artist': "Исполнитель",
            'release_year': "Год выпуска",
            'genre': "Жанр",
            'duration': "Продолжительность",
        }
        help_texts = {
            'duration': "Например: 00:45:30 или 45 минут",
        }

    def clean_release_year(self):
        year = self.cleaned_data['release_year']
        if year < 1900 or year > 2030:
            raise forms.ValidationError("Введите корректный год выпуска (1900-2030).")
        return year
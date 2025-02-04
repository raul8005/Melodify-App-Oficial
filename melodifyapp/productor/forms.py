from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=True,
        label="Buscar canción o álbum",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Nombre de la canción o álbum'}),
    )

    
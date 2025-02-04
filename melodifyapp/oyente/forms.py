from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=True,
        label="Buscar artista o canción",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Nombre del artista o canción'}),
    )
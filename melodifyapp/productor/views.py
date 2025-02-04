from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from musico.forms import MessageForm
from django.shortcuts import render
from musico.models import Favorite, LikeDislike, Message, Song
from .forms import SearchForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def search_song_productor(request):
    form = SearchForm(request.GET or None)
    results = []
    query = ""

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Song.objects.filter(
            Q(title__icontains=query) |
            Q(album__title__icontains=query) |
            Q(album__musician__first_name__icontains=query) &
            Q(album__musician__last_name__icontains=query) |
            Q(album__musician__first_name__icontains=query) |
            Q(album__musician__last_name__icontains=query) 
        ).distinct()

    return render(request, 'productor/buscar_artista_productor.html', {
        'form': form,
        'results': results,
        'query': query,
    })


def reproduce_music_productor(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    is_favorited = Favorite.objects.filter(user=request.user, song=song).exists()


    return render(request, 'productor/reproductor_musica_productor.html', {
        'song': song,
        'is_favorited': is_favorited,  # Pasamos esta variable al contexto
    })
@login_required
def send_message_productor(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    artist = song.album.musician

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = artist
            message.save()
            return redirect('productor:reproduce_music_productor', song_id=song.id)
    else:
        form = MessageForm()

    return render(request, 'productor/send_message_productor.html', {
        'form': form,
        'song': song,
        'artist': artist,
    })

@login_required
def add_to_favorites(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, song=song)
    if created:
        messages.success(request, f"'{song.title}' ha sido agregado a tus favoritos.")
    else:
        messages.info(request, f"'{song.title}' ya está en tus favoritos.")
    return redirect('productor:reproduce_music_productor', song_id=song.id)

@login_required
def remove_from_favorites(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    favorite = Favorite.objects.filter(user=request.user, song=song)
    if favorite.exists():
        favorite.delete()
        messages.success(request, f"'{song.title}' ha sido eliminado de tus favoritos.")
    else:
        messages.info(request, f"'{song.title}' no estaba en tus favoritos.")
    return redirect('productor:reproduce_music_productor', song_id=song.id)

@login_required
def messages_sent(request):
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'productor/messages_sent.html', {'messages': messages})
@login_required
def favorite_songs(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('song__album')
    return render(request, 'productor/favorites_songs.html', {'favorites': favorites})
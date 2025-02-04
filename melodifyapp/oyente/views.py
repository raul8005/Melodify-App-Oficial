from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from musico.models import Song, Album, LikeDislike
from users.models import User
from users.models import Follow
from .forms import SearchForm
from django.contrib.auth.decorators import login_required

def search_artist(request):
    """Vista para buscar artistas, canciones o álbumes."""
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

    return render(request, 'oyente/buscar_artista.html', {
        'form': form,
        'results': results,
        'query': query,
    })


def comment_song(request, song_id):
    from musico.models import Comment, Song
    from musico.forms import CommentForm

    song = Song.objects.get(id=song_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.song = song
            comment.save()
            return redirect('oyente:reproduce_music', song_id=song_id)
    else:
        form = CommentForm()

    return render(request, 'musico/add_comment.html', {'form': form, 'song': song})

@login_required
def reproduce_music(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    # Obtener los IDs de los artistas que el usuario está siguiendo
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)

    user_vote = None
    if request.user.is_authenticated:
        vote = LikeDislike.objects.filter(user=request.user, song=song).first()
        if vote:
            user_vote = 'like' if vote.vote == LikeDislike.LIKE else 'dislike'

    return render(request, 'oyente/reproductor_musica.html', {
        'song': song,
        'user_vote': user_vote,
        'following_ids': list(following_ids),  # Añadido
    })
def like_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    like, created = LikeDislike.objects.get_or_create(user=request.user, song=song, defaults={'vote': LikeDislike.LIKE})
    if not created and like.vote == LikeDislike.LIKE:
        like.delete()
    elif not created:
        like.vote = LikeDislike.LIKE
        like.save()
    return redirect('oyente:reproduce_music', song_id=song.id)

def dislike_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    dislike, created = LikeDislike.objects.get_or_create(user=request.user, song=song, defaults={'vote': LikeDislike.DISLIKE})
    if not created and dislike.vote == LikeDislike.DISLIKE:
        dislike.delete()
    elif not created:
        dislike.vote = LikeDislike.DISLIKE
        dislike.save()
    return redirect('oyente:reproduce_music', song_id=song.id)

@login_required
def album_list_oyente(request):
    albums = Album.objects.all().prefetch_related('songs', 'artist')
    return render(request, 'musico/album_list_oyente.html', {'albums': albums})

def album_detail_oyente(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    songs = album.songs.all()
    return render(request, 'oyente/album_detail_oyente.html', {
        'album': album,
        'songs': songs,
    })
@login_required
def liked_songs(request):
    liked_songs = Song.objects.filter(likedislike__user=request.user, likedislike__vote=LikeDislike.LIKE).distinct()
    return render(request, 'oyente/liked_songs.html', {'liked_songs': liked_songs})

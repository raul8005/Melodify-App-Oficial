from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import Follow, User
from .models import Album, Song, Comment, Message
from .forms import AlbumForm, SongForm, CommentForm, MessageForm
from django.core.paginator import Paginator
from mutagen.mp3 import MP3 

@login_required
def create_album(request):
    if request.method == "POST":
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.musician = request.user
            album.save()
            return redirect('musico:album_list')
    else:
        form = AlbumForm()
    return render(request, 'musico/crear_album.html', {'form': form})

@login_required
def upload_music(request, album_id):
    album = get_object_or_404(Album, id=album_id, musician=request.user)
    
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            new_song = form.save(commit=False)
            new_song.album = album
            new_song.save()  # La duración ahora se calcula dentro del método save()
            return redirect('musico:album_detail', album_id=album.id)
    
    else:
        form = SongForm()
    
    return render(request, 'musico/upload_music.html', {'form': form, 'album': album})

@login_required
def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id, musician=request.user)
    songs = album.songs.all()
    
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            new_song = form.save(commit=False)
            new_song.album = album
            new_song.save()
            return redirect('musico:album_detail', album_id=album.id)
    else:
        form = SongForm()
    
    return render(request, 'musico/album_detail.html', {
        'album': album,
        'songs': songs,
        'form': form
    })

@login_required
def song_list(request):
    songs = Song.objects.filter(album__musician=request.user)
    return render(request, 'musico/song_list.html', {'songs': songs})

@login_required
def add_comment(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.song = song
            comment.save()
            return redirect('musico:add_comment', song_id=song.id)  # Redirige a la misma página
    else:
        form = CommentForm()
    return render(request, 'musico/add_comment.html', {'form': form, 'song': song})


@login_required
def comments_received(request):
    # Recupera todas las canciones del músico actual
    songs = Song.objects.filter(album__musician=request.user)
    
    # Recupera todos los comentarios de esas canciones
    comments = Comment.objects.filter(song__in=songs).order_by('-created_at')
    
    # Filtros de búsqueda
    search_query = request.GET.get('search', '')
    song_filter = request.GET.get('song', '')
    
    if search_query:
        comments = comments.filter(content__icontains=search_query)
    
    if song_filter:
        comments = comments.filter(song__id=song_filter)
    
    # Paginación: 10 comentarios por página
    paginator = Paginator(comments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener la lista de canciones para el filtro
    songs_list = songs.order_by('title')
    
    return render(request, 'musico/comments_received.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'song_filter': song_filter,
        'songs_list': songs_list,
    })
@login_required
def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id, album__musician=request.user)
    comments = song.comments.all().order_by('-created_at')
    
    return render(request, 'musico/song_detail.html', {'song': song, 'comments': comments})
@login_required
def album_list(request):
    albums = Album.objects.filter(musician=request.user)
    return render(request, 'musico/album_list.html', {'albums': albums})

@login_required
def send_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('musico:message_list')
    else:
        form = MessageForm()
    return render(request, 'musico/send_message.html', {'form': form})

@login_required
def message_list(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'musico/message_list.html', {'messages': messages})

@login_required
def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id, musician=request.user)
    songs = album.songs.all()
    return render(request, 'musico/album_detail.html', {'album': album, 'songs': songs})

@login_required
def edit_album(request, album_id):
    album = get_object_or_404(Album, id=album_id, musician=request.user)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('musico:album_list')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'musico/edit_album.html', {'form': form, 'album': album})

@login_required
def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id, musician=request.user)
    if request.method == 'POST':
        album.delete()
        return redirect('musico:album_list')
    return render(request, 'musico/delete_album.html', {'album': album})


@login_required
def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id, album__musician=request.user)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect('musico:album_detail', album_id=song.album.id)
    else:
        form = SongForm(instance=song)
    return render(request, 'musico/edit_song.html', {'form': form, 'song': song})

@login_required
def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id, album__musician=request.user)
    if request.method == 'POST':
        album_id = song.album.id
        song.delete()
        return redirect('musico:album_detail', album_id=album_id)
    return render(request, 'musico/delete_song.html', {'song': song})



@login_required
def follow_artist(request, artist_id):
    artista = get_object_or_404(User, id=artist_id, user_type='M')
    seguimiento, created = Follow.objects.get_or_create(follower=request.user, following=artista)
    if not created:
        seguimiento.delete()
    return redirect('musico:following_artists')

@login_required
def following_artists(request):
    seguimientos = Follow.objects.filter(follower=request.user).select_related('following')
    return render(request, 'musico/following_artists.html', {
        'seguimientos': seguimientos,
    })
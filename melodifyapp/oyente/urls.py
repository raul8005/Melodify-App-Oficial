from django.urls import path
from . import views

app_name = 'oyente'

urlpatterns = [
    path('buscar-artista/', views.search_artist, name='search_artist'),
    path('canciones/<int:song_id>/comentar/', views.comment_song, name='comment_song'),
    path('canciones/<int:song_id>/reproducir/', views.reproduce_music, name='reproduce_music'),
    path('canciones/<int:song_id>/like/', views.like_song, name='like_song'),
    path('canciones/<int:song_id>/dislike/', views.dislike_song, name='dislike_song'),
    path('album/<int:album_id>/', views.album_detail_oyente, name='album_detail_oyente'),  
    path('liked-songs/', views.liked_songs, name='liked_songs'),

]

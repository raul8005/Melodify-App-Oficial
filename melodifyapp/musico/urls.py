from django.urls import path
from . import views

app_name = 'musico'

urlpatterns = [
    path('create-album/', views.create_album, name='create_album'),
    path('album/<int:album_id>/upload_music/', views.upload_music, name='upload_music'),  
    path('songs/', views.song_list, name='song_list'),
    path('songs/<int:song_id>/comment/', views.add_comment, name='add_comment'),
    path('album-list/', views.album_list, name='album_list'),
    path('messages/', views.message_list, name='message_list'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('album/<int:album_id>/edit/', views.edit_album, name='edit_album'),    
    path('album/<int:album_id>/delete/', views.delete_album, name='delete_album'),
    path('song/<int:song_id>/edit/', views.edit_song, name='edit_song'),       
    path('song/<int:song_id>/delete/', views.delete_song, name='delete_song'),
    path('comments-received/', views.comments_received, name='comments_received'),

    path('song/<int:song_id>/', views.song_detail, name='song_detail'),
    path('seguir-artista/<int:artist_id>/', views.follow_artist, name='follow_artist'),
    path('artistas-seguidos/', views.following_artists, name='following_artists'),

]

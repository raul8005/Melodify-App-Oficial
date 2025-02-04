from django.urls import path
from . import views

app_name = 'productor'

urlpatterns = [
    path('buscar-canciones/', views.search_song_productor, name='search_song_productor'),
    path('canciones/<int:song_id>/reproducir/', views.reproduce_music_productor, name='reproduce_music_productor'),
    path('song/<int:song_id>/send_message/', views.send_message_productor, name='send_message_productor'),
    path('song/<int:song_id>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('song/<int:song_id>/unfavorite/', views.remove_from_favorites, name='remove_from_favorites'),
    path('mensajes-enviados/', views.messages_sent, name='messages_sent'),  
    path('favoritos/', views.favorite_songs, name='favorite_songs'),  


]
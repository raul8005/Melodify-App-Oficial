from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Importa el modelo de usuario configurado

class Album(models.Model):
    title = models.CharField(max_length=100)
    musician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="albums")
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)

    def __str__(self):
        return self.title
    
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

class Song(models.Model):
    title = models.CharField(max_length=255)
    album = models.ForeignKey('Album', related_name='songs', on_delete=models.CASCADE)
    file = models.FileField(upload_to='songs/')
    duration = models.PositiveIntegerField(default=0)  # Guardamos la duración en segundos
    song_cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Calcula y almacena la duración antes de guardar la canción."""
        if self.file:
            try:
                audio = MP3(self.file)
                self.duration = int(audio.info.length)  # Convierte a segundos
            except Exception as e:
                self.duration = 0  # En caso de error, establece la duración en 0

        super(Song, self).save(*args, **kwargs)

    def get_duration_display(self):
        """Devuelve la duración en formato MM:SS"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"

    def __str__(self):
        return f"{self.title} ({self.get_duration_display()})"
 
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.user} en {self.song.title}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"

class LikeDislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey('musico.Song', on_delete=models.CASCADE)  # Evita referencias circulares
    LIKE = 1
    DISLIKE = -1
    CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    )
    vote = models.SmallIntegerField(choices=CHOICES)

    class Meta:
        unique_together = ('user', 'song') 
class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    song = models.ForeignKey(
        'musico.Song',
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')

    def __str__(self):
        return f"{self.user.first_name} - {self.song.title}"
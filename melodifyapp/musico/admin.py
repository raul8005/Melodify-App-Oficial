from django.contrib import admin
from .models import Album, Song, Comment, Message
# Register your models here.
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'musician', 'release_date')
    search_fields = ('title', 'musician__username')
    list_filter = ('release_date',)
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'duration')
    search_fields = ('title', 'album__title')
    list_filter = ('album__release_date',)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'created_at')
    search_fields = ('user__username', 'song__title')
    list_filter = ('created_at',)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp')
    search_fields = ('sender__username', 'recipient__username')
    list_filter = ('timestamp',)

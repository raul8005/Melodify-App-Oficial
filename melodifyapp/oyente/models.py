from django.db import models

from django.db import models
from django.conf import settings

class ListenerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listener_profile")
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


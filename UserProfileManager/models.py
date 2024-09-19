from django.conf import settings
from django.db import models
from gestion_contenus.models import Film  # Assurez-vous que ce chemin est correct

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.CharField(max_length=20, default='fr')
    video_quality = models.CharField(max_length=20, default='HD')

class WatchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film', 'watched_at')

class FavoriteList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film')

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from gestion_contenus.models import Film  # Assurez-vous que Film est bien le modèle pour les films

class Commentaire(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='commentaires')
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commentaire de {self.utilisateur.username} sur {self.film.titre}'

class Avis(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='avis')
    note = models.PositiveIntegerField()  # Note sur une échelle de 1 à 5, par exemple
    commentaire = models.TextField(blank=True, null=True)  # Optionnel, l'utilisateur peut juste donner une note
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Avis de {self.utilisateur.username} sur {self.film.titre}'

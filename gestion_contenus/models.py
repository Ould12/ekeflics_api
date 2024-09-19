
# Create your models here.
# models.py

from django.db import models

class Genre(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Film(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='films')
    date_de_sortie = models.DateField()
    duree = models.DurationField()  # Ex: 1:30:00
    image = models.URLField()  # URLField for images
    video = models.URLField()  # URLField for videos
    acteurs = models.CharField(max_length=255)  # Actor names as a comma-separated string
    producteurs = models.CharField(max_length=255)  # Producer names as a comma-separated string

    def __str__(self):
        return self.titre

class Serie(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='series')
    date_de_sortie = models.DateField()
    image = models.URLField()

    def __str__(self):
        return self.titre

class Saison(models.Model):
    serie = models.ForeignKey(Serie, related_name='saisons', on_delete=models.CASCADE)
    numero_saison = models.IntegerField()
    date_de_sortie = models.DateField()

    def __str__(self):
        return f"{self.serie.titre} - Saison {self.numero_saison}"

class Episode(models.Model):
    saison = models.ForeignKey(Saison, related_name='episodes', on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    numero_episode = models.IntegerField()
    duree = models.DurationField()
    video = models.URLField()

    def __str__(self):
        return f"Série: {self.saison.serie.titre} - Saison {self.saison.numero_saison} - Episode {self.numero_episode}: {self.titre}"


class EvenementLive(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_evenement = models.DateTimeField()
    genre = models.ManyToManyField(Genre, related_name='evenements')
    lien_streaming = models.URLField(max_length=200)
    image = models.ImageField(upload_to='evenements/')

    def __str__(self):
        return self.titre

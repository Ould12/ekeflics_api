from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from .models import Film, Serie, Saison, Episode, EvenementLive, Genre
from .serializers import FilmSerializer, SerieSerializer, SaisonSerializer, EpisodeSerializer, EvenementLiveSerializer, GenreSerializer

class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [IsAdminUser]  # Only admins can create/update/delete films

class SerieViewSet(viewsets.ModelViewSet):
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer
    permission_classes = [IsAdminUser]  # Only admins can create/update/delete series

class SaisonViewSet(viewsets.ModelViewSet):
    queryset = Saison.objects.all()
    serializer_class = SaisonSerializer
    permission_classes = [IsAdminUser]  # Only admins can create/update/delete seasons

class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAdminUser]  # Only admins can create/update/delete episodes

class EvenementLiveViewSet(viewsets.ModelViewSet):
    queryset = EvenementLive.objects.all()
    serializer_class = EvenementLiveSerializer
    permission_classes = [IsAdminUser]  # Only admins can create/update/delete live events

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]  # Only admins can create/update/delete genres

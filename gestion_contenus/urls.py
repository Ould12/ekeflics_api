from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FilmViewSet, SerieViewSet, SaisonViewSet, EpisodeViewSet, EvenementLiveViewSet, GenreViewSet

router = DefaultRouter()
router.register(r'films', FilmViewSet)
router.register(r'series', SerieViewSet)
router.register(r'saisons', SaisonViewSet)
router.register(r'episodes', EpisodeViewSet)
router.register(r'evenements', EvenementLiveViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

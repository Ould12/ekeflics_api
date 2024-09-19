from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentaireViewSet, AvisViewSet

router = DefaultRouter()
router.register(r'commentaires', CommentaireViewSet)
router.register(r'avis', AvisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

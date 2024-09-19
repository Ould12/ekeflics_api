from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Commentaire, Avis
from .serializers import CommentaireSerializer, AvisSerializer

class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

class AvisViewSet(viewsets.ModelViewSet):
    queryset = Avis.objects.all()
    serializer_class = AvisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

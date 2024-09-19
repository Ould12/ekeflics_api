from rest_framework import serializers
from .models import Commentaire, Avis

class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ['id', 'utilisateur', 'film', 'texte', 'date_creation']
        read_only_fields = ['id', 'utilisateur', 'date_creation']

class AvisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avis
        fields = ['id', 'utilisateur', 'film', 'note', 'commentaire', 'date_creation']
        read_only_fields = ['id', 'utilisateur', 'date_creation']

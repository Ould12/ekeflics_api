# serializers.py

from rest_framework import serializers
from .models import Film, Serie, Episode, EvenementLive, Genre, Saison

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'nom']
        


class FilmSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ['id', 'titre', 'description', 'genre', 'duree', 'date_de_sortie', 'image', 'video', 'acteurs', 'producteurs']

    def create(self, validated_data):
        film = Film.objects.create(**validated_data)
        return film

    def update(self, instance, validated_data):
        instance.titre = validated_data.get('titre', instance.titre)
        instance.description = validated_data.get('description', instance.description)
        instance.date_de_sortie = validated_data.get('date_de_sortie', instance.date_de_sortie)
        instance.duree = validated_data.get('duree', instance.duree)
        instance.image = validated_data.get('image', instance.image)
        instance.video = validated_data.get('video', instance.video)
        instance.acteurs = validated_data.get('acteurs', instance.acteurs)
        instance.producteurs = validated_data.get('producteurs', instance.producteurs)
        instance.save()
        return instance



class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'

class SaisonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Saison
        fields = ['id', 'serie', 'numero_saison', 'date_de_sortie', 'episodes']

class SerieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    saisons = SaisonSerializer(many=True, read_only=True)

    class Meta:
        model = Serie
        fields = ['id', 'titre', 'description', 'genre', 'date_de_sortie', 'image', 'saisons']


class EvenementLiveSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = EvenementLive
        fields = '__all__'

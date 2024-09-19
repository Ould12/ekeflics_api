from rest_framework import serializers
from .models import UserProfile, WatchHistory, FavoriteList
from gestion_contenus.models import Film

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['language', 'video_quality']

class WatchHistorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    film = serializers.PrimaryKeyRelatedField(queryset=Film.objects.all())

    class Meta:
        model = WatchHistory
        fields = ['user', 'film', 'watched_at']
        read_only_fields = ['user']

class FavoriteListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    film = serializers.PrimaryKeyRelatedField(queryset=Film.objects.all())

    class Meta:
        model = FavoriteList
        fields = ['user', 'film', 'added_at']
        read_only_fields = ['user']

# serializers.py
from rest_framework import serializers
from .models import Notification, NotificationPreference, PushSubscription
from django.contrib.auth import get_user_model
User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # Ajoute le username dans les données en sortie
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), write_only=True)  # Utiliser le `username` pour créer la notification

    class Meta:
        model = Notification
        fields = ['id', 'user', 'username', 'title', 'message', 'sent_at']  # Assurez-vous d'inclure 'user' dans les fields
        read_only_fields = ['sent_at', 'username']  # 'username' et 'sent_at' sont en lecture seule

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['user', 'email_notifications', 'push_notifications']

class PushSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushSubscription
        fields = ['id', 'user', 'endpoint', 'p256dh', 'auth', 'created_at']

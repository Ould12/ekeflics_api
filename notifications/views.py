from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response  # Correct import for Response
from rest_framework import generics, permissions
from .models import Notification, NotificationPreference, PushSubscription
from .serializers import NotificationSerializer, NotificationPreferenceSerializer, PushSubscriptionSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

from django.core.mail import send_mail
from django.conf import settings

class NotificationListCreateView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]  # Seuls les admins peuvent créer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Récupérer l'utilisateur cible à partir du `username` fourni dans le corps de la requête
        username = self.request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        # Sauvegarder la notification pour cet utilisateur
        notification = serializer.save(user=user)

        # Vérifier les préférences de notification
        notification_preference = NotificationPreference.objects.get(user=user)
        
        # Envoyer un email si l'utilisateur a activé les notifications par email
        if notification_preference.email_notifications:
            self.send_notification_email(user.email, notification.title, notification.message)

    def send_notification_email(self, to_email, title, message):
        subject = f"Nouvelle notification: {title}"
        email_message = f"Vous avez une nouvelle notification :\n\n{message}"
        send_mail(
            subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Récupérer ou créer une préférence de notification pour l'utilisateur connecté
        notification_preference, created = NotificationPreference.objects.get_or_create(user=self.request.user)
        return notification_preference



class PushSubscriptionListCreateView(generics.ListCreateAPIView):
    serializer_class = PushSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PushSubscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

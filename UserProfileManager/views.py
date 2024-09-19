from rest_framework import generics, permissions
from .models import UserProfile, WatchHistory, FavoriteList
from .serializers import UserProfileSerializer, WatchHistorySerializer, FavoriteListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class UserProfileView(APIView):
    def get(self, request):
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            # Créer le UserProfile si il n'existe pas
            profile = UserProfile.objects.create(user=request.user)
        
        # Retourner les données du profil ici
        return Response(UserProfileSerializer(profile).data)

    def put(self, request):
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        
        # Mettre à jour les préférences de l'utilisateur
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

class WatchHistoryView(generics.ListCreateAPIView):
    serializer_class = WatchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchHistory.objects.filter(user=self.request.user)

class FavoriteListView(generics.ListCreateAPIView):
    serializer_class = FavoriteListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

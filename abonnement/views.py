from rest_framework import generics, permissions
from .models import Subscription, SubscriptionPlan
from .serializers import SubscriptionSerializer, SubscriptionPlanSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

class SubscriptionListCreateView(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubscriptionPlanCreateView(generics.CreateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminUser]  # Seuls les administrateurs peuvent créer des plans

class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class SubscriptionPlanListView(generics.ListAPIView):
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SubscriptionPlan.objects.all()

class SubscriptionActivateView(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user, is_active=False)

    def update(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.activate()
        return Response({'status': 'Subscription activated'}, status=status.HTTP_200_OK)

class SubscriptionDeactivateView(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user, is_active=True)

    def update(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.deactivate()
        return Response({'status': 'Subscription deactivated'}, status=status.HTTP_200_OK)

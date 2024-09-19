from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import generics, permissions
from .models import ViewingStatistics, ContentPerformance, UserEngagement, Content
from .serializers import ViewingStatisticsSerializer, ContentPerformanceSerializer, UserEngagementSerializer, ContentSerializer

class ViewingStatisticsListView(generics.ListAPIView):
    serializer_class = ViewingStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ViewingStatistics.objects.filter(user=self.request.user)

class ContentPerformanceListView(generics.ListAPIView):
    serializer_class = ContentPerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContentPerformance.objects.all()

class UserEngagementDetailView(generics.RetrieveAPIView):
    serializer_class = UserEngagementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserEngagement.objects.filter(user=self.request.user)

class ContentListView(generics.ListAPIView):
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Content.objects.all()

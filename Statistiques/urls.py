# urls.py
from django.urls import path
from .views import (
    ViewingStatisticsListView,
    ContentPerformanceListView,
    UserEngagementDetailView,
    ContentListView
)

urlpatterns = [
    path('viewing-statistics/', ViewingStatisticsListView.as_view(), name='viewing-statistics-list'),
    path('content-performance/', ContentPerformanceListView.as_view(), name='content-performance-list'),
    path('user-engagement/', UserEngagementDetailView.as_view(), name='user-engagement-detail'),
    path('content/', ContentListView.as_view(), name='content-list'),
]

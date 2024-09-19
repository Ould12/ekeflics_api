# urls.py
from django.urls import path
from .views import (
    NotificationListCreateView,
    NotificationDetailView,
    NotificationPreferenceView,
    PushSubscriptionListCreateView
)

urlpatterns = [
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('notification-preferences/', NotificationPreferenceView.as_view(), name='notification-preference'),
    path('push-subscriptions/', PushSubscriptionListCreateView.as_view(), name='push-subscription-list-create'),
]

from django.urls import path
from .views import (
    SubscriptionListCreateView,
    SubscriptionDetailView,
    SubscriptionPlanCreateView,
    SubscriptionPlanListView,
    SubscriptionActivateView,
    SubscriptionDeactivateView
)

urlpatterns = [
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='subscription-list-create'),
    path('subscriptions/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('subscription-plans/', SubscriptionPlanListView.as_view(), name='subscription-plan-list'),
    path('create-subscription-plan/', SubscriptionPlanCreateView.as_view(), name='create-subscription-plan'),
    path('subscriptions/activate/', SubscriptionActivateView.as_view(), name='subscription-activate'),
    path('subscriptions/deactivate/', SubscriptionDeactivateView.as_view(), name='subscription-deactivate'),
]

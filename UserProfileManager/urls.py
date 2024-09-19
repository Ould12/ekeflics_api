from django.urls import path
from .views import UserProfileView, WatchHistoryView, FavoriteListView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('history/', WatchHistoryView.as_view(), name='watch_history'),
    path('favorites/', FavoriteListView.as_view(), name='favorite_list'),
]

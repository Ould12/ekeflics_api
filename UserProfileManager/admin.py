from django.contrib import admin
from .models import UserProfile, WatchHistory, FavoriteList
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(WatchHistory)
admin.site.register(FavoriteList)
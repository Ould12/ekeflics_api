from django.contrib import admin

# Register your models here.
from .models import Notification,NotificationPreference,PushSubscription

# Register your models here.
admin.site.register(Notification)
admin.site.register(NotificationPreference)
admin.site.register(PushSubscription)
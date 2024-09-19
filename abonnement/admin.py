from django.contrib import admin

# Register your models here.
from .models import Subscription,SubscriptionPlan

# Register your models here.
admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
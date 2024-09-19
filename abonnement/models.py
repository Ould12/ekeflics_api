from django.conf import settings
from django.db import models
from django.utils import timezone

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    billing_history = models.JSONField(default=dict)  # Store billing history as JSON

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

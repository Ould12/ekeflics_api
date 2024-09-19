from django.db import models
from abonnement.models import Subscription  # Importer le modèle Subscription

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="transactions", null=True, blank=True)  # Relier à l'abonnement

    def __str__(self):
        return f"Transaction ID: {self.transaction_id}, Amount: {self.amount}, Status: {self.status}, Customer: {self.customer_name}"

from django.urls import path
from .views import (
    initiate_payment,
    payment_notification,
    payment_success  # Importer la vue pour le succès du paiement

)

urlpatterns = [
    path('payment/', initiate_payment, name='initiate-payment'),
    path('payment/notify/', payment_notification, name='payment-notification'),
    path('payment-success/', payment_success, name='payment-success'),  # URL pour le succès du paiement

]

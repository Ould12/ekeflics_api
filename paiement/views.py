from django.utils import timezone
import random
import requests
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from abonnement.models import Subscription, SubscriptionPlan
from .models import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from dateutil.relativedelta import relativedelta



CINETPAY_API_KEY = settings.CINETPAY_API_KEY
CINETPAY_SITE_ID = settings.CINETPAY_SITE_ID

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    if request.method == 'POST':
        user = request.user
        customer_name = f"{user.first_name} {user.last_name}"
        customer_email = user.email
        amount = request.data.get('amount')
        plan_id = request.data.get('plan_id')  # Récupérer l'ID du plan d'abonnement

        if not amount or not plan_id:
            return JsonResponse({'error': 'Le montant et le plan sont requis'}, status=400)

        # Récupérer le plan d'abonnement
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        start_date = timezone.now().date()
        end_date = start_date + relativedelta(months=plan.duration_months)

        # Créer l'abonnement avant de démarrer le paiement
        subscription = Subscription.objects.create(
            user=user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            is_active=False,  # L'abonnement sera activé après le paiement
            billing_history={}
        )

        # Créer une transaction liée à cet abonnement
        transaction_id = str(random.randint(1000000, 9999999))
        transaction = Transaction.objects.create(
            transaction_id=transaction_id,
            amount=amount,
            customer_name=customer_name,
            customer_email=customer_email,
            subscription=subscription  # Lier la transaction à l'abonnement
        )

        data = {
            'apikey': CINETPAY_API_KEY,
            'site_id': CINETPAY_SITE_ID,
            'transaction_id': transaction_id,
            'amount': amount,
            'currency': 'XOF',
            'description': 'Paiement pour commande',
            'customer_name': customer_name,
            'customer_email': customer_email,
            'notify_url': 'http://localhost:8000/api/payment/notify/',  # URL de notification
            'return_url': 'http://localhost:8000/api/payment-success/',
            'channels': 'ALL'
        }

        response = requests.post('https://api-checkout.cinetpay.com/v2/payment', json=data)

        if response.status_code == 200:
            payment_data = response.json()
            return JsonResponse({'payment_url': payment_data['data']['payment_url']})
        else:
            return JsonResponse({'error': 'Erreur lors de la création du paiement'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
@api_view(['POST'])
def payment_notification(request):
    if request.method == 'POST':
        data = request.data
        transaction_id = data.get('transaction_id')
        status = data.get('status')

        try:
            # Rechercher la transaction par son ID
            transaction = Transaction.objects.get(transaction_id=transaction_id)

            if status == 'ACCEPTED':
                # Activer l'abonnement lié à la transaction
                subscription = transaction.subscription
                subscription.activate()
                transaction.status = 'ACCEPTED'  # Mettre à jour le statut de la transaction
            elif status == 'REFUSED':
                subscription = transaction.subscription
                subscription.deactivate()
                transaction.status = 'REFUSED'

            transaction.save()  # Sauvegarder la transaction après mise à jour du statut
            return JsonResponse({'status': 'success'})

        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'Transaction not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def payment_success(request):
    # Vous pouvez ajouter ici toute logique nécessaire après un paiement réussi
    return render(request, 'paiements/payment_success.html', context={'message': 'Votre paiement a été effectué avec succès !'})
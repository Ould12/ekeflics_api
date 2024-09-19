# views.py

from sqlite3 import IntegrityError
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework_simplejwt.tokens import RefreshToken
from .tokens import account_activation_token
from .serializers import RegisterSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        password = request.data.get('password')
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Lien de réinitialisation invalide.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Lien de réinitialisation invalide.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({'message': 'Mot de passe réinitialisé avec succès.'}, status=status.HTTP_200_OK)

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'L\'adresse e-mail est inconnue.'}, status=status.HTTP_400_BAD_REQUEST)

        # Envoyer un e-mail avec le lien de réinitialisation
        current_site = get_current_site(request)
        mail_subject = 'Réinitialisez votre mot de passe'
        protocol = 'https' if request.is_secure() else 'http'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        message = render_to_string('account/password_reset_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
            'protocol': protocol,
        })
        plain_message = strip_tags(message)
        send_mail(mail_subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=message)

        return Response({'message': 'Un e-mail de réinitialisation du mot de passe a été envoyé.'}, status=status.HTTP_200_OK)

class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))  # Utiliser force_str ici
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Votre compte a été activé. Vous pouvez maintenant vous connecter.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Le lien de confirmation est invalide ou a expiré.'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # L'utilisateur doit confirmer son email
            user.save()

            # Envoyer un email de confirmation
            current_site = get_current_site(request)
            mail_subject = 'Confirmez votre adresse email'
            protocol = 'https' if request.is_secure() else 'http'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            # Impressions pour débogage
            print(f'Protocol: {protocol}')
            print(f'Domain: {current_site.domain}')
            print(f'UID: {uid}')
            print(f'Token: {token}')

            message = render_to_string('account/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'protocol': protocol,
            })
            
            # Impression du message pour vérifier son contenu
            print(f'Email message: {message}')

            send_mail(
                mail_subject,
                strip_tags(message),  # Texte brut pour les clients qui ne supportent pas HTML
                settings.EMAIL_HOST_USER,
                [user.email],
                html_message=message  # Email au format HTML
            )

            return Response({'message': 'Utilisateur créé avec succès. Veuillez confirmer votre email.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        mot_de_passe = data.get('mot_de_passe')

        # Récupérer l'utilisateur avec l'e-mail
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

        # Vérifier le mot de passe
        if not user.check_password(mot_de_passe):
            return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Vérifier si l'utilisateur est actif
        if not user.is_active:
            return Response({'error': 'Votre email n\'a pas été confirmé. Veuillez vérifier votre email.'}, status=status.HTTP_403_FORBIDDEN)

        # Générer et retourner le token JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
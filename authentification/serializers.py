# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    mot_de_passe = serializers.CharField(write_only=True)
    numero_whatsapp = serializers.CharField(max_length=20, required=False, allow_blank=True)
    code_parrainage = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['prenom'],
            last_name=validated_data['nom'],
            password=make_password(validated_data['mot_de_passe']),
        )
        return user

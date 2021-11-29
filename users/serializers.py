from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.postgres.fields import JSONField
from drf_yasg import openapi
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(min_length=1, max_length=255, write_only=True,
                                               style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password',
                  'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        confirmed_password = self.validated_data['confirmed_password']

        if confirmed_password != password:
            raise serializers.ValidationError({'password': 'Please enter matched passwords.'})
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']


# Serializers for Swagger

class SwaggerRegistrationSerializer(serializers.Serializer):
    detail = 'The user is successfully created.'
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()


class SwaggerTokenObtainPairSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class SwaggerTokenRefreshSerializer(serializers.Serializer):
    access = serializers.CharField()


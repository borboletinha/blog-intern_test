from rest_framework import serializers
from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(min_length=1, max_length=255, write_only=True,
                                               style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password',
                  'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = CustomUser(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        confirmed_password = self.validated_data['confirmed_password']

        if confirmed_password != password:
            raise serializers.ValidationError({'password': 'Please enter matched passwords'})
        user.set_password(user.password)
        user.save()
        return user

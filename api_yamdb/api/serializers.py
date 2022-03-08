from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class SignupUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                f'Пользователь с почтой {value} уже есть в базе'
            )
        return value

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя `me` в качестве username запрещено.'
            )
        return value


class TokenSerializer(serializers.Serializer):

    confirmation_code = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=30)

    def validate_confirmation_code(self, value):
        user = get_object_or_404(User, username=self.initial_data['username'])
        if not default_token_generator.check_token(user=user, token=value):
            raise serializers.ValidationError(
                'Неверный `confirmation_code` или истёк его срок годности.'
            )
        return value

    def create(self, validated_data):
        return validated_data

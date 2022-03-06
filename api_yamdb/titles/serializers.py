from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import Category, Genre, Title
from .validators import UserFollowValidator

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Title


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
        required=False
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        read_only=False,
        many=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Нельзя подписаться на не существующего пользователя'
            )]
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Такая подписка уже существует'
            ),
            UserFollowValidator(),
        ]

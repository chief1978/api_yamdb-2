from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()


class SignupUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)
        extra_kwargs = {'email': {'required': True}}

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

    def validate(self, data):
        user = get_object_or_404(
            User,
            username=data.get('username')
        )
        if not default_token_generator.check_token(
            user=user,
            token=data.get('confirmation_code')
        ):
            raise serializers.ValidationError(
                'Неверный `confirmation_code` или истёк его срок годности.'
            )
        return data

    def create(self, validated_data):
        return validated_data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        #lookup_field = 'slug'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        #lookup_field = 'slug'
        model = Genre


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = GenreTitle


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True, required=False)
    genre = GenreSerializer(many=True, read_only=True, required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role',
        )
        extra_kwargs = {'email': {'required': True}}

    def validate(self, data):
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким `email` уже зарегистрирован.'
            )
        return data


class OneUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role',
        )


class MyselfSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role',
        )
        extra_kwargs = {'role': {'read_only': True}}


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug'
    )

    def validate(self, data):
        if data['score'] not in range(1, 11):
            raise serializers.ValidationError(
                "Оценка должна быть в диапазоне [1, 10]"
            )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Comment

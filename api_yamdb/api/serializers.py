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
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = GenreTitle


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            titles = Title.objects.create(**validated_data)
            return titles
        genres = validated_data.pop('genre')
        titles = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = get_object_or_404(Genre, slug=genre)
            GenreTitle.objects.create(genre_id=current_genre, title_id=titles)
        return titles


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

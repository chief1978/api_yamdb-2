from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Category, Genre, GenreTitle, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        required=False,
        slug_field='slug'
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genre')
        title = Title.objects.update(**validated_data)
        for genre_data in genres_data:
            genre = get_object_or_404(Genre, slug=genre_data['slug'])
            GenreTitle.objects.create(genre=title, genre_id=genre)
        return title

from django.shortcuts import get_object_or_404
from rest_framework import serializers


from .models import Category, Genre, GenreTitle, Title


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
    category = CategorySerializer(many=False, read_only=True, required=False)
    genre = GenreSerializer(many=True, read_only=True, required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title      

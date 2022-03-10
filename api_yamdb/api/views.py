from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Category, Genre, GenreTitle, Title
from .permissions import IsAdminOrReadOnlyPermission
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', 'name', 'year')
    search_fields = ('name',)

    def get_queryset(self):
        queryset = Title.objects.all().order_by('id')
        genre = self.request.query_params.get('genre')
        if genre is not None:
            genre = get_object_or_404(Genre, slug=genre)
            title_list = GenreTitle.objects.values_list(
                'title_id', flat=True).filter(genre_id=genre)
            queryset = Title.objects.filter(id__in=title_list).order_by('id')
        return queryset

    def perform_create(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        title = serializer.save(category=category)
        genres_data = self.request.data['genre']
        for genre_data in genres_data:
            genre = get_object_or_404(Genre, slug=genre_data)
            GenreTitle.objects.create(title_id=title, genre_id=genre)

    def perform_update(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        title = serializer.save(category=category)
        title.genre.clear()
        genres_data = self.request.data['genre']
        for genre_data in genres_data:
            genre = get_object_or_404(Genre, slug=genre_data)
            GenreTitle.objects.create(title_id=title, genre_id=genre)

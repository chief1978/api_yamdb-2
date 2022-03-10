from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Category, Genre, GenreTitle, Title
from .permissions import IsAdminOrReadOnlyPermission
from .serializers import SignupUserSerializer, TokenSerializer, CategorySerializer, GenreSerializer, TitleSerializer

User = get_user_model()


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = SignupUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(password='1234')
        code = default_token_generator.make_token(serializer.instance)
        send_mail(
            subject='confirmation_code',
            message=(
                f'{serializer.instance.username} your '
                f'confirmation_code: {code}'
            ),
            from_email='server@mail.fake',
            recipient_list=[serializer.instance.email]
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.save()
        user = get_object_or_404(User, username=data['username'])
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response(
            {'token': token},
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


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

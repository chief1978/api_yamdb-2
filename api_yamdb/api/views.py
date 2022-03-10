from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, GenreTitle, Title
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer, GenreSerializer, MyselfSerializer,
    SignupUserSerializer, TitleSerializer, TokenSerializer, UsersSerializer,
)

User = get_user_model()


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
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
@permission_classes((permissions.AllowAny,))
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.save()
        user = get_object_or_404(User, username=data['username'])
        user.password = ''
        user.save()
        token = str(AccessToken.for_user(user))
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
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTTokenUserAuthentication,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
    lookup_value_regex = "[^/]+"


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTTokenUserAuthentication,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
    lookup_value_regex = "[^/]+"


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


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UsersSerializer
    lookup_field = 'username'
    lookup_url_kwargs = 'username'
    lookup_value_regex = r'[\w.@+-]+'

    def get_object(self):
        if self.kwargs.get('username', None) == 'me':
            self.kwargs['username'] = self.request.user.username
        return super(UsersViewSet, self).get_object()


class MyselfViewSet(APIView):

    def get_object(self, username):
        return get_object_or_404(User, username=username)

    def get(self, request):
        user = self.get_object(request.user.username)
        serializer = MyselfSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = self.get_object(request.user.username)
        serializer = MyselfSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

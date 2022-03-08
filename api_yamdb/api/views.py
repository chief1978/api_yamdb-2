from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupUserSerializer, TokenSerializer

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

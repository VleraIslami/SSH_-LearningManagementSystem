import random
from django.shortcuts import render

from api import serializer as api_serializer
from userauths.models import User, Profile


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_frameword.permission import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer


def generate_random_opt(Length=7):
    opt = ''.join([str(random.randint(0, 9))for _ in range(Length)])
    return opt


def PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):

    permission_class = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def get_object(self):
        # api/v1/passsword-email ... e merr url prej ktu
        email = self.kwargs['email']

        # shko ne db edhe e merr email e e pare te user ku email qe e zgjedhem
        # lart eshre e njejte me email dhe nese ska nuk ekzkeutohet hiq
        user = User.objects.filter(email=email).first()

        if user:
            # identify a user by token
            uuidb64 = user.pk

            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            user.refresh_token = refresh_token

            user.opt = generate_random_opt()
            user.save()

            # localhost e ndrron qysh te pershtatet
            # duhet me pas nje refresh token
            link = f"htpp://localhost:5173/create-new-password/?opt={user.opt}&uuidb64={uuidb64}&=refresh_token{refresh_token}"
            print("link=====", link)

        return user

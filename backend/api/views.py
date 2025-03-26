from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from api import serializer as api_serializer
from userauths.models import User, Profile


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

import random


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer


def generate_random_opt(Length=7):
    opt = ''.join([str(random.randint(0, 9))for _ in range(Length)])
    return opt


class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):

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

            context = {
                "link": link,
                "username": user.username
            }

            subject = "Password Reset Email"
            text_body = render_to_string("email/password_reset.txt", context)
            html_body = render_to_string("email/password_reset.html", context)

            msg = EmailMultiAlternatives
            (
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[user.email],
                body=text_body
            )

            msg.attach_alternative(html_body, "text/html")
            msg.send()

            print("link=====", link)

        return user

# create e new pass for a user


class PasswordChangeApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # cilido user mundet me acces kete pjese
    serializer_class = api_serializer.UserSerializer

    def create(self, request, *args, **kwargs):

        # krejt infot i marrim prej request data per opt pass  edhe 64
        opt = request.data['opt']
        uuidb64 = request.data['uuidb64']
        password = request.data['password']

        # fetch the user me data qe i kemi prej larte
        user = User.objects.get(id=uuidb64, opt=opt)
        if user:  # nese user exits we set the data pass opt dhe e bojm save
            user.set_password(password)
            user.opt = ""
            user.save()

            return Response({"message": "Password changed successfully"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"message": "User Does Not Exists"}, status=status.HTTP_404_NOT_FOUND)

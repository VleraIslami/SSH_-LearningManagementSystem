from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from api import serializer as api_serializer
from api import models as api_models
from userauths.models import User, Profile

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

import random
from decimal import Decimal


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
            link = f"htpp://localhost:5173/create-new-password/?opt={user.opt}&uuidb64={uuidb64}&refresh_token{refresh_token}"

            context = {
                "link": link,
                "username": user.username
            }

            subject = "Password Reset Email"
            text_body = render_to_string("email/password_reset.txt", context)
            html_body = render_to_string("email/password_reset.html", context)

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.FROM_EMAIL,
                to=[user.email]
            )

            msg.attach_alternative(html_body, "text/html")
            msg.send()

    #     msg = EmailMultiAlternatives(
    # subject=subject,
    # from_email=settings.FROM_EMAIL,
    # to=[user.email],
    # body=text_body
    #         )

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

class CategoryListAPIView(generics.ListAPIView):
    queryset = api_models.Category.objects.filter(active=True)
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]

class CourseListAPIView(generics.ListAPIView):
    queryset = api_models.Course.objects.filter(platform_status = "Published", teacher_course_status = "Published")
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]

class CourseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]
    queryset = api_models.Course.objects.filter(platform_status = "Published", teacher_course_status = "Published")

    # www.website-url.com/lms-website-using-django-and-react/

    def get_object(self):
        slug = self.kwargs['slug']
        course = api_models.Course.objects.get(slug=slug, platform_status = "Published", teacher_course_status = "Published")
        return course


class CartAPIView(generics.CreateAPIView):
    queryset = api_models.Cart.objects.all()
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        course_id = request.data['course_id'] #ne kit mnyr i marrim te dhanat
        user_id = request.data['user_id']
        price = request.data['price']
        country_name = request.data['country_name']
        cart_id = request.data['cart_id']

        # tash per me i barazu id e krejtve e perdorim first qe me marr tparin qe pershtatet
        course = api_models.Course.objects.filter(id=course_id).first()
        #user = User.objects.filter(id=user_id).first() # qikjo na prun error se nese ska usera ska qa kthen
        #e bojm ni kusht if else nese ka usera
        if user_id is "undefined":
            user = User.objects.filter(id=user_id).first()
        else:
            user = None

        #e bojm te njejtin sen me country 
        try:
            country_object = api_models.Country.objects.filter(name= country_name).first()  
            country = country_object.name
        except:
            country_object = None
            country = "United States" #default value
        
        if country_object:
            tax_rate = country_object.tax_rate /100
        else:
            tax_rate = 0

        cart = api_models.Cart.objects.filter(cart_id=cart_id, course=course).first()

        if cart:
            cart.course = course
            cart.user = user
            cart.price = price 
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(price) + Decimal( cart.tax_fee)
            cart.save()

            return Response({"message": "Cart updated successfully"}, status=status.HTTP_200_OK)
        else:
            cart =api_models.Cart()

            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(price) + Decimal(cart.tax_fee)
            cart.save()
            return Response({"message": "Cart created successfully"}, status=status.HTTP_201_CREATED)
        
class CartListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        queryset = api_models.Cart.objects.filter(cart_id=cart_id)
        return queryset

class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        cart_id = self.kwargs['cart_id']
        item_id = self.kwargs['item_id']

        return api_models.Cart.objects.get(cart_id=cart_id, id=item_id).first()
        # e bojm delete

class CartStatsAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'cart_id'

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        queryset = api_models.Cart.objects.filter(cart_id=cart_id)
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        total_price = 0.00
        total_tax = 0.00
        total_total = 0.00

        #iterojm neper secilin antare t queryset
        for cart_item in queryset:
            total_price += float(self.calculate_price(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_total += round(float(self.calculate_total(cart_item)), 2) # 2 nr mas presjes
            # e bojm totalin

        data ={
             "price": total_price, #12 
             "tax": total_tax, 
             "total": total_total 

        }
        return Response(data)

    def calculate_price(self, cart_item):
        return cart_item.price 
        # e bojm totalin
    
    def calculate_tax(self, cart_item):
        return cart_item.tax_fee
        # e bojm taxin

    def calculate_total(self, cart_item):
        return cart_item.total
        # e bojm totalin

class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.CartOrderItemSerializer
    permission_classes = [AllowAny]
    queryset = api_models.CartOrder.objects.all()

    def create(self, request, *args, **kwargs):
        full_name = request.data['full_name']
        email = request.data['email']
        country = request.data['country']
        cart_id = request.data['cart_id']
        user_id = request.data['user_id']

        if user_id !=0:
            user = User.objects.get(id=user_id)
        else:
            user = None
        
        cart_items = api_models.Cart.objects.filter(cart_id=cart_id)

        total_price = Decimal(0.00)
        total_tax = Decimal(0.00)
        total_initial_total = Decimal(0.00)
        total_total = Decimal(0.00)

        order = api_models.CartOrder.objects.create(
            full_name = full_name,
            email = email,
            country = country,
            student = user
        )

        for c in cart_items:
            api_models.CartOrderItem.objects.create(
                order = order,
                course = c.course,
                price = c.price,
                tax_fee = c.tax_fee,
                total = c.total,
                initial_total = c.total,
                teacher = c.course.teacher
            )

            total_price += Decimal(c.price)
            total_tax += Decimal(c.tax_fee)
            total_initial_total += Decimal(c.total)
            total_total += Decimal(c.total)

            order.teachers.add(c.course.teacher)

        order.sub_total = total_price  
        order.tax_fee = total_tax
        order.initial_total = total_initial_total
        order.total = total_total
        order.save()

        return Response({"message": "Order Created Successfully"}, status= status.HTTP_201_CREATED)


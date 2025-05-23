from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.hashers import change_password, check_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import models


from api import serializer as api_serializer
from api import models as api_models
from userauths.models import Profile

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from datetime import datetime,timedelta
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
            link = f"http://localhost:5173/create-new-password/?opt={user.opt}&uuidb64={uuidb64}&refresh_token={refresh_token}"

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


#class enrollmend [po mungon] 

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



class ChangePasswordAPIView(generics.APIView):
    serializer_class = api_serializer.UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        user=User.objects.get(id=user_id)
        if user is not None:
            if check_password(old_password, user.password):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password changed successfully", "icon": "success"})
            else:
                return Response({"message": "Old password is incorrect", "icon": "warning"})
        else:
            return Response({"message": "User does not exist", "icon": "error"})






class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = api_serializer.ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return Profile.objects.get(user=user)


class CategoryListAPIView(generics.ListAPIView):
    queryset = api_models.Category.objects.filter(active=True)
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]



class CourseListAPIView(generics.ListAPIView):
    queryset = api_models.Course.objects.filter(
        platform_status="Published", teacher_course_status="Published")
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]


class CourseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]
    queryset = api_models.Course.objects.filter(
        platform_status="Published", teacher_course_status="Published")

    # www.website-url.com/lms-website-using-django-and-react/

    def get_object(self):
        slug = self.kwargs['slug']
        course = api_models.Course.objects.get(
            slug=slug, platform_status="Published", teacher_course_status="Published")
        return course


class CartAPIView(generics.CreateAPIView):
    queryset = api_models.Cart.objects.all()
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        course_id = request.data['course_id']  # ne kit mnyr i marrim te dhanat
        user_id = request.data['user_id']
        price = request.data['price']
        country_name = request.data['country_name']
        cart_id = request.data['cart_id']

        print("course_id ===", course_id)

        # tash per me i barazu id e krejtve e perdorim first qe me marr tparin qe pershtatet
        course = api_models.Course.objects.filter(id=course_id).first()
        # user = User.objects.filter(id=user_id).first() # qikjo na prun error se nese ska usera ska qa kthen
        # e bojm ni kusht if else nese ka usera
        if user_id is "undefined":
            user = User.objects.filter(id=user_id).first()
        else:
            user = None

        # e bojm te njejtin sen me country
        try:
            country_object = api_models.Country.objects.filter(
                name=country_name).first()
            country = country_object.name
        except:
            country_object = None
            country = "United States"  # default value

        if country_object:
            tax_rate = country_object.tax_rate / 100
        else:
            tax_rate = 0

        cart = api_models.Cart.objects.filter(
            cart_id=cart_id, course=course).first()

        if cart:
            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(price) + Decimal(cart.tax_fee)
            cart.save()

            return Response({"message": "Cart updated successfully"}, status=status.HTTP_200_OK)
        else:
            cart = api_models.Cart()

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

        # iterojm neper secilin antare t queryset
        for cart_item in queryset:
            total_price += float(self.calculate_price(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            # 2 nr mas presjes
            total_total += round(float(self.calculate_total(cart_item)), 2)
            # e bojm totalin

        data = {
            "price": total_price,  # 12
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

        if user_id != 0:
            user = User.objects.get(id=user_id)
        else:
            user = None

        cart_items = api_models.Cart.objects.filter(cart_id=cart_id)

        total_price = Decimal(0.00)
        total_tax = Decimal(0.00)
        total_initial_total = Decimal(0.00)
        total_total = Decimal(0.00)

        order = api_models.CartOrder.objects.create(
            full_name=full_name,
            email=email,
            country=country,
            student=user
        )

        for c in cart_items:
            api_models.CartOrderItem.objects.create(
                order=order,
                course=c.course,
                price=c.price,
                tax_fee=c.tax_fee,
                total=c.total,
                initial_total=c.total,
                teacher=c.course.teacher
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

        return Response({"message": "Order Created Successfully", "order_oid":order.oid}, status=status.HTTP_201_CREATED)


class CheckoutAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.CartOrderSerializer
    permission_classes = [AllowAny]
    queryset = api_models.CartOrder.objects.all()
    lookup_field = 'oid'


class CouponApplyAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.CouponSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        order_oid = request.data['order_oid']
        coupon_code = request.data['coupon_code']

        order = api_models.CartOrder.objects.get(oid=order_oid)
        coupon = api_models.Coupon.objects.get(code=coupon_code)

        if coupon:
            order_items = api_models.CartOrderItem.objects.filter(
                order=order, teacher=coupon.teacher)
            for i in order_items:
                if not coupon in i.coupons.all():
                    discount = i.total * coupon.discount/100

                    i.total = i.total - discount
                    i.price = i.price - discount
                    i.saved = i.saved + discount
                    i.applied_coupon = True
                    i.coupons.add(coupon)

                    order.coupons.add(coupon)
                    order.total -= discount
                    order.sub_total -= discount
                    order.saved += discount

                    i.save()
                    order.save()
                    # sa user e kan use coupon
                    coupon.used_by.add(order.student)

                    return Response({"message": "Coupon Found and Activated"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "Coupon Already Applied"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Coupon Not Found"}, status=status.HTTP_404_NOT_FOUND)



#payment
#
#

class SearchCourseAPIView(generics.ListAPIView):
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.GET.get('query')
        return api_models.Course.objects.filter(title__icontains=query, platform_status="Published", teacher_course_status="Published")
        
class StudentSummaryAPIView(generics.ListAPIView):
    serializer_class = api_serializer.StudentSummarySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        total_courses = api_models.EnrolledCourse.objects.filter(user=user).count()
        completed_lesson = api_models.CompletedLesson.objects.filter(user=user).count()
        achieved_certificates = api_models.Certificate.objects.filter(user=user).count()

        return [{
            "total_courses": total_courses,
            "completed_lesson": completed_lesson,
            "achieved_certificates": achieved_certificates,
        }]
    
    def list(self, request , *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StudentCourseListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.EnrolledCourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return api_models.EnrolledCourse.objects.filter(user=user)

class StudentCourseDetailAPIView(generics.ListAPIView):
    serializer_class = api_serializer.EnrolledCourseSerializer
    permission_classes = [AllowAny]
    lookup_field = 'enrollment_id'

    def get_object(self):
        user_id = self.kwargs['user_id']
        enrollment_id = self.kwargs['enrollment_id']

        user =User.objects.get(id=user_id)
        return api_models.EnrolledCourse.objects.get(user=user, enrollment_id=enrollment_id)

class StudentCourseCompletedCreateAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.CompletedLessonSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']
        variant_item_id = request.data['variant_item_id']

        user = User.objects.get(id=user_id)
        course = api_models.Course.objects.get(id=course_id)
        variant_item = api_models.VariantItem.objects.get(variant_item_id=variant_item_id)

        completed_lessons = api_models.CompletedLesson.objects.filter(user=user, course=course, variant_item=variant_item).first()

        if completed_lessons:
            completed_lessons.delete()
            return Response({"message" : "Course marked as not completed"})
        else:
            api_models.CompletedLesson.objects.create(user=user, course=course, variant_item=variant_item)
            return Response({"message": "Lesson marked as completed"})

class StudentNoteCreateAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.NoteSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.request.data['user_id']
        enrollment_id = self.request.data['enrollment_id']

        user = User.objects.get(id=user_id)
        enrolled = api_models.EnrolledCourse.objects.get(enrollment_id=enrollment_id)
        return api_models.Note.objects.filter(user=user, course=enrolled.course)

    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        enrollment_id = request.data['enrollment_id']
        title=request.data['title']
        note=request.data['note']

        user = User.objects.get(id=user_id)
        enrolled = api_models.EnrolledCourse.objects.get(enrollment_id=enrollment_id)

        api_models.Note.objects.create(user=user, course=enrolled.course, note=note, title=title)

        return Response({"message": "Note Created Successfully"}, status=status.HTTP_201_CREATED)

#     {
#     "user_id": 1,
#     "enrollment_id": "2485",
#     "title": " Anote",
#      "note": "Vlera created  a note"
#   }
     
class StudentNoteDetailAPIView(generics.ListAPIView):
    serializer_class = api_serializer.NoteSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        enrollment_id = self.kwargs['enrollment_id']
        note_id = self.kwargs['note_id']

        user = User.objects.get(id=user_id)
        enrolled = api_models.EnrolledCourse.objects.get(enrollment_id=enrollment_id)
        note= api_models.Note.objects.filter(user=user, course=enrolled.course, id=note_id)
        return note

class StudentRateCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.ReviewSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']
        rateing = request.data['rating']
        review = request.data['review']

        user = User.objects.get(id=user_id)
        course = api_models.Course.objects.get(id=course_id)

        api_models.Review.objects.create(
            user=user, 
            course=course, 
            review=review, 
            rating=rateing,
            active=True,
            )

        return Response({"message": "Reviwe Created Successfully"}, status=status.HTTP_201_CREATED)


#{
#"user_id": 1,
#"course_id": 1,
#"rating": 5,
#"review": "VERY NICE COURSE"
#}


class StudentRateCourseUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = api_serializer.ReviewSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        reviwe_id = self.kwargs['review_id']

        user = User.objects.get(id=user_id)
        return api_models.Review.objects.get(id=reviwe_id,user=user)

def update_password_view(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        new_password = request.POST.get("new_password")
        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            return JsonResponse({"message": "Password updated successfully!"})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

class StudentWishListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = api_serializer.WishListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return api_models.WishList.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']

        user = User.objects.get(id=user_id)
        course = api_models.Course.objects.get(id=course_id)

        wishlist = api_models.WishList.objects.filter(user=user, course=course).first()
        if wishlist:
            wishlist.delete()
            return Response({"message": "Wishlist Deleted!"}, status=status.HTTP_200_OK)
        else:
            api_models.WishList.objects.create(user=user, course=course)
            return Response({"message": "Wishlist created!"}, status=status.HTTP_201_CREATED)
       

class QuestionAnswerListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = api_serializer.Question_AnswerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = api_models.Course.objects.get(id=course_id)
        return api_models.Question_Answer.objects.filter(course=course)
    
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']
        title = request.data['title']
        message = request.data['message']

        user = User.objects.get(id=user_id)
        course = api_models.Course.objects.get(id=course_id)

        question =api_models.Question_Answer.objects.filter(user=user, course=course , title=title )

        api_models.Question_Answer.objects.create(user=user, course=course, message=message, question=question)

        return Response({"message": "Group conversation started!"}, status=status.HTTP_201_CREATED)
    


class QuestionAnswerMessageSendAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.Question_AnswerSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']
        qa_id = request.data['qa_id']
        message = request.data['message']

        user = User.objects.get(id=user_id)
        course = api_models.Course.objects.get(id=course_id)

        question =api_models.Question_Answer.objects.filter(qa_id= qa_id )

        api_models.Question_Answer.objects.create(user=user, course=course, message=message, question=question)
        question_serializer = api_serializer.Question_AnswerSerializer(question)

        return Response({"message": "Message sent!", "question": question_serializer.data})







class TeacherSummaryAPIView(generics.ListAPIView):
    serializer_class = api_serializer.TeacherSummarySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = api_models.Teacher.objects.get(id=teacher_id)

       one_month_ago = datetime.now() - timedelta(days=28)
       
       total_courses = api_models.Course.objects.filter(teacher=teacher).count()
       total_revenue = api_models.CartOrderItem.objects.filter(teacher=teacher, order_payment_status="Paid").aggregate(total_revenue=models.Sum("price"))["total_revenue"]or 0   
       monthly_revenue = api_models.CartOrderItem.objects.filter(teacher=teacher, order_payment_status="Paid",date_gte=one_month_ago).aggregate(total_revenue=models.Sum("price")["total_revenue"]or 0)

   
       enrolled_course=api_models.EnrolledCourse.objects.filter(teacher=teacher)
       unique_students_ids = set(_)
       students=[]

       for course in enrolled_courses:
           if course.user_id not in unique_student_ids:
              user=User.objects.get(id=course.user_id)
               student={
                "full_name": user.profile.first_name,
                "image": user.profile.image.url,
                "country":user.profile.country,,
                "date":course.data
         }



            students.append(student)
            unique_student_ids.add(course.user_id)

        return [{
            total_courses: total_courses,
            "total_revenue": total_revenue,
            "monthly_revenue": monthly_revenue,
            "total_students""len(students),
        }]

    def list(self, request , *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
from api import views as api_views
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # Authentication Endpoints

    path("user/token/", api_views.MyTokenObtainPairView.as_view()),
    path("user/token/refresh/", TokenRefreshView.as_view()),
    path("user/register/", api_views.RegisterView.as_view()),
    path("user/password-reset/<email>/",
         api_views.PasswordResetEmailVerifyAPIView.as_view()),
    # ka mundesi del nje error si  no such coulumn userauths_user.refresh_token
    # edhe duhet me shku me ndez serverin(makemigrations) pastaj migrate (13)
    path("user/password-change/", api_views.PasswordChangeApiView.as_view()),
    path("user/profile/user_id>/", api_views.ProfileAPIView.as_view()),
    path("user/change-password/", api_views.ChangePasswordAPIView.as_view()),


    # Core Endpoints
    path("course/category/", api_views.CategoryListAPIView.as_view()),
    path("course/course-list/", api_views.CourseListAPIView.as_view()),
    path("course/course-detail/<slug>",
         api_views.CourseDetailAPIView.as_view()),
    path("course/search/", api_views.SearchCourseAPIView.as_view()),
    path("course/cart/", api_views.CartAPIView.as_view()),
    path("course/cart-list/<cart_id>", api_views.CartListAPIView.as_view()),
    path("course/cart-item-delete/<cart_id>/<item_id>/",
         api_views.CartItemDeleteAPIView.as_view()),
    path("cart/stats/<cart_id>/", api_views.CartStatsAPIView.as_view()),
    path("order/create-order/", api_views.CreateOrderAPIView.as_view()),
    path("order/checkout/<int:oid>", api_views.CheckoutAPIView.as_view()),
    path("order/coupon/", api_views.CouponApplyAPIView.as_view()),


     #Student API Endpoints
     path("student/summary/<user_id>/", api_views.StudentSummaryAPIView.as_view()),
     path("student/course-list/<user_id>/", api_views.StudentCourseListAPIView.as_view()),
     path("student/course-detail/<user_id>/<enrollment_id>/", api_views.StudentCourseListAPIView.as_view()),
     path("student/course-completed/", api_views.StudentCourseCompletedCreateAPIView.as_view()),
]

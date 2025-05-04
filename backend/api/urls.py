from api import views as api_views
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("user/token/", api_views.MyTokenObtainPairView.as_view()),
    path("user/token/refresh/", TokenRefreshView.as_view()),
    path("user/register/", api_views.RegisterView.as_view()),
    path("user/password-reset/<email>/",
         api_views.PasswordResetEmailVerifyAPIView.as_view()),
    # ka mundesi del nje error si  no such coulumn userauths_user.refresh_token
    # edhe duhet me shku me ndez serverin(makemigrations) pastaj migrate (13)
    path("user/password-change/", api_views.PasswordChangeApiView.as_view())
] 
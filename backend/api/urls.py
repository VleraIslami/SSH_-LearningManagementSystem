from api import views as api_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView


from rest_framework import parmissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Learnin system",
        default_version='v1',
        terms_of_service="https://www.google.com/policies/terms",
        contatct=openapi.Contact(email="vleraislami11@gmail.com"),
        license=openapi.License(name="BSD License"),

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('', schema_view.with_ui('swagger', cashe_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-swagger-ui'),





    path('admin/', admin.site.urls),

    path("api/v1/", include("api.urls"))

]


urlpatterns = [
    path("user/token/", api_views.MyTokenObtainPairView.as_view()),
    path("user/token/refresh/", TokenRefreshView.as_view()),
    path("user/register/", api_views.RegisterView.as_view()),
    path("user/password-reset/<email>/",
         api_views.PasswordResetEmailVerifyAPIView.as_view()),
    # ka mundesi del nje error si  no such coulumn userauths_user.refresh_token
    # edhe duhet me shku me ndez serverin(makemigrations) pastaj migrate (13)
    path("user/password-change/", api_views.PasswordChangeAPIView.as_view())
]

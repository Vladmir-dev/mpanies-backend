from django.urls import path
from .views import UserRegistrationView, UserLoginView, AdminLoginView, UserLogoutView
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import re_path as url

schema_view = get_schema_view(
   openapi.Info(
      title="Mpanies API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('admin/register/', UserRegistrationView.as_view(), name='admin-registration'),  # Admin registration endpoint
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    # Other URL patterns
]

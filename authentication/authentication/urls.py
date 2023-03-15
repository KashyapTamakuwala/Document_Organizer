"""authentication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Users.views import Register
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/register',Register.as_view(),name="Register"),
    #path('user/login',ObtainAuthToken.as_view(),name="Login"),
    path('user/login',TokenObtainPairView.as_view(),name="Login"),
    path('user/verify',TokenVerifyView.as_view(),name="Verification"),
    path('user/refresh',TokenRefreshView.as_view(),name="Refersh Access Token")

]
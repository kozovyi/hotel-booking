"""
URL configuration for hotel_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from modules.user.views import UserRegisterView


router = routers.DefaultRouter()

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),
    
    #auth
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/jwt/create/', TokenObtainPairView.as_view(), name="jwt_create"),
    path('api/v1/auth/jwt/refresh/', TokenRefreshView.as_view(), name="jwt_refresh"),


    #user
    path('api/v1/register/', UserRegisterView.as_view(), name='user_register'),

    #main api
    path('api/v1/', include(router.urls)),
]
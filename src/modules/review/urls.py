from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from modules.review.views import ReviewViewSet
#from rest_framework import routers

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
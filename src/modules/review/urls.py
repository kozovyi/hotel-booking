from django.contrib import admin
from django.urls import path, include
from modules.review import views
#from rest_framework import routers

urlpatterns = [
    path('reviews/', views.review_list),
    path('reviews/<int:pk>/', views.current_review_detail),
]
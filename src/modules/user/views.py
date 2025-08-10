from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from modules.user.models import User
from modules.user.serializer import UserRegisterSerializer


# Create your views here.
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny,]
    
    

from rest_framework import serializers

from modules.user.models import User
from modules.user.service import UserService


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return UserService.create(**validated_data)

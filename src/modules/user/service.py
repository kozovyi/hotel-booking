from django.contrib.auth import get_user_model


User = get_user_model()


class UserService:
    @classmethod
    def create(cls, **validated_data):
        return User.objects.create_user(**validated_data)

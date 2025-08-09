from modules.user.models import User


class UserService():

    @classmethod
    def create(cls, **validated_data):
        return User.objects.create_user(**validated_data)
        